from django.contrib import admin
from .models import Show, Season, Episode, Image


class ShowAdmin(admin.ModelAdmin):
    search_fields = ("title", "slug", "tvdb_id", "tv_maze_id")


class SeasonAdmin(admin.ModelAdmin):
    search_fields = ("show",)


class EpisodeAdmin(admin.ModelAdmin):
    search_fields = ("title", "tvdb_id",)


# Register your models here.
admin.site.register(Show, ShowAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(Image)
