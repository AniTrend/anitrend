from django.contrib import admin
from .models import XemTitle, Xem


class XemAdmin(admin.ModelAdmin):
    search_fields = ("id",)


class XemTitleAdmin(admin.ModelAdmin):
    search_fields = ("title", "xem__id")


# Register your models here.
admin.site.register(Xem, XemAdmin)
admin.site.register(XemTitle, XemTitleAdmin)
