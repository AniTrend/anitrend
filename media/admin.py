from django.contrib import admin
from .models import Media, Source, Airing, Season, MetaData, Information, Episode, Image


class MediaAdmin(admin.ModelAdmin):
    search_fields = ("title",)


class SourceAdmin(admin.ModelAdmin):
    search_fields = ("anilist", "tvdb", "mal")


# Register your models here.
admin.register(Media, MediaAdmin)
admin.register(Source, SourceAdmin)
admin.register(Airing,)
admin.register(Season,)
admin.register(MetaData,)
admin.register(Information,)
admin.register(Episode,)
admin.register(Image,)
