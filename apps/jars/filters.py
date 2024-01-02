from django.db.models import QuerySet, ExpressionWrapper, F, fields, OuterRef, Subquery
from django_filters import rest_framework as filters

from .models import Jar, JarCurrentSum

FILTER_CHOICES = (
    ('fill_percentage', 'fill_percentage - ascending'),
    ('-fill_percentage', 'fill_percentage - descending'),
)


class JarFilter(filters.FilterSet):
    """filter for Jar"""
    fill_percentage = filters.ChoiceFilter(
        choices=FILTER_CHOICES,
        method='filter_fill_percentage'
    )

    class Meta:
        model = Jar
        fields = ['fill_percentage']

    def filter_fill_percentage(self, queryset, name, value) -> QuerySet:
        # filtered_queryset = queryset.annotate(
        #         fill_percentage=ExpressionWrapper(
        #             F('jarcurrentsum__sum') * 100.0 / F('goal'),
        #             output_field=fields.FloatField()
        #         )
        #     ).order_by(value)
        subquery = JarCurrentSum.objects.filter(jar=OuterRef('pk')).order_by('-date_added')
        queryset = queryset.annotate(
            latest_sum=Subquery(subquery.values('sum')[:1]),
            fill_percentage=F('latest_sum') * 100.0 / F('goal'),
        ).order_by(value)
        return queryset
