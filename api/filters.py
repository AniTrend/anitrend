from django_filters import FilterSet, CharFilter, OrderingFilter
import api.models


class SeriesPagingFilter(FilterSet):
    # Do case-insensitive lookups on 'title'
    title = CharFilter(lookup_expr=['iexact'])

    class Meta:
        model = api.models.Series
        fields = ["title"]

    order_by = OrderingFilter(
        fields=(
            ("title"),
        )
    )
