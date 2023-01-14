from django_filters import FilterSet, CharFilter, OrderingFilter
from media.models import Media


class MediaPagingFilterSet(FilterSet):
    # Do case-insensitive lookups on 'title'
    title = CharFilter(lookup_expr=['iexact'])

    class Meta:
        model = Media
        fields = ["title"]

    order_by = OrderingFilter(
        fields=(
            ("title"),
        )
    )
