from django_filters import FilterSet, CharFilter, ChoiceFilter, NumberFilter, OrderingFilter
import api.models


class SeriesPagingFilter(FilterSet):
    # Do case-insensitive lookups on 'title'
    title = CharFilter(lookup_expr=['iexact'])
    status = ChoiceFilter(choices=api.models.STATUS_CHOICES)

    class Meta:
        model = api.models.Series
        fields = ["title", "status"]

    order_by = OrderingFilter(
        fields=(
            ("title"),
        )
    )


class SeriesFilter(FilterSet):
    tvdb = NumberFilter()
    anilist = NumberFilter()

    class Meta:
        model = api.models.Series
        fields = ["tvdb", "anilist"]
