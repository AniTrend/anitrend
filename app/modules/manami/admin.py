from django.contrib import admin
from .models import Anime, AnimeRelation, AnimeSource


class AnimeAdmin(admin.ModelAdmin):
    search_fields = ("title",)


class AnimeSourceAdmin(admin.ModelAdmin):
    search_fields = ("anidb", "anilist", "animeplanet", "kitsu", "mal", "notify",)


class AnimeRelationAdmin(admin.ModelAdmin):
    search_fields = ("url", "anime__title",)


# Register your models here.
admin.site.register(Anime, AnimeAdmin)
admin.site.register(AnimeSource, AnimeSourceAdmin)
admin.site.register(AnimeRelation, AnimeRelationAdmin)
