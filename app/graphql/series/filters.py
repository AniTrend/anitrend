from django_filters import FilterSet, CharFilter, OrderingFilter
from ...modules.series.models import Series


class SeriesPagingFilterSet(FilterSet):
    # Do case-insensitive lookups on 'title'
    title = CharFilter(lookup_expr=['iexact'])

    class Meta:
        model = Series
        fields = ["title"]

    order_by = OrderingFilter(
        fields=(
            ("title"),
        )
    )
