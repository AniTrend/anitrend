from django.contrib import admin

from config.models import DefaultImage, Settings, Config

# Register your models here.
admin.site.register(DefaultImage)
admin.site.register(Settings)
admin.site.register(Config)
