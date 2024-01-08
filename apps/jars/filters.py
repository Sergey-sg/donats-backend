from django.db.models import QuerySet, F, OuterRef, Subquery
from django_filters import rest_framework as filters

from .models import Jar, AmountOfJar

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
    /api/jars/?fill_percentage=-fill_percentage
    ```

    Query Parameters:
        - `fill_percentage`: Filter jars by fill percentage.

    Choices:
        - "fill_percentage": Ascending order
        - "-fill_percentage": Descending order

    """
    fill_percentage = filters.ChoiceFilter(
        choices=FILTER_CHOICES,
        method='filter_fill_percentage'
    )

    class Meta:
        model = Jar
        fields = ['fill_percentage']

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
