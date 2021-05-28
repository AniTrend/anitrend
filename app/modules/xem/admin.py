from django.contrib import admin
from .models import Xem


class XemAdmin(admin.ModelAdmin):
    search_fields = ("id",)


# Register your models here.
admin.site.register(Xem, XemAdmin)
