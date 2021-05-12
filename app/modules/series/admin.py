from django.contrib import admin
from .models import Series, Source, Relation


class SeriesAdmin(admin.ModelAdmin):
    search_fields = ("title",)


class SourceAdmin(admin.ModelAdmin):
    search_fields = ("anilist", "tvdb", "mal")


# Register your models here.
admin.site.register(Series, SeriesAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Relation)
