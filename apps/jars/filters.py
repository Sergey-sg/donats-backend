from django.db.models import QuerySet, F, OuterRef, Subquery
from django_filters import rest_framework as filters

from .models import Jar, AmountOfJar, JarTag

FILTER_CHOICES = (
    ('fill_percentage', 'fill_percentage - ascending'),
    ('-fill_percentage', 'fill_percentage - descending'),
)


class JarFilter(filters.FilterSet):
    """
    Filter for Jar model.

    Supports filtering by fill percentage.

    Example:
    ```
    /api/jars/?fill_percentage=-fill_percentage&tags=name
    ```

    Query Parameters:
        - `fill_percentage`: Filter jars by fill percentage.
        - `tags`: Filter by tags name.

    Choices:
        - "fill_percentage": Ascending order
        - "-fill_percentage": Descending order

    """
    fill_percentage = filters.ChoiceFilter(
        choices=FILTER_CHOICES,
        method='filter_fill_percentage'
    )
    tags = filters.ModelChoiceFilter(
        queryset=JarTag.objects.all(),
        field_name="tags",
        to_field_name='name',
    )

    class Meta:
        model = Jar
        fields = ['fill_percentage', 'tags']

    def filter_fill_percentage(self, queryset, name, value) -> QuerySet:
        """
        Filter jars based on fill percentage.

        Args:
            queryset (QuerySet): The queryset to be filtered.
            name (str): The name of the filter field.
            value (str): The selected filter value.

        Returns:
            QuerySet: The filtered queryset.
        """
        subquery = AmountOfJar.objects.filter(
            jar=OuterRef('pk')).order_by('-date_added')
        queryset = queryset.annotate(
            latest_sum=Subquery(subquery.values('sum')[:1]),
            fill_percentage=F('latest_sum') * 100.0 / F('goal'),
        ).order_by(value)
        return queryset
