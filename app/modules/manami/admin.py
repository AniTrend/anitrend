from django.contrib import admin
from .models import Anime, AnimeSource


class AnimeAdmin(admin.ModelAdmin):
    search_fields = ("title",)


class AnimeSourceAdmin(admin.ModelAdmin):
    search_fields = ("anidb", "anilist", "animeplanet", "kitsu", "mal", "notify",)


# Register your models here.
admin.register(Anime, AnimeAdmin)
admin.register(AnimeSource, AnimeSourceAdmin)
