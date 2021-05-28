from django.contrib import admin
from .models import Series, Source, Airing, Season, MetaData, Information, Episode, Image


class SeriesAdmin(admin.ModelAdmin):
    search_fields = ("title",)


class SourceAdmin(admin.ModelAdmin):
    search_fields = ("anilist", "tvdb", "mal")


# Register your models here.
admin.site.register(Series, SeriesAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Airing,)
admin.site.register(Season,)
admin.site.register(MetaData,)
admin.site.register(Information,)
admin.site.register(Episode,)
admin.site.register(Image,)
