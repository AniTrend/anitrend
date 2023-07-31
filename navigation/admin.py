from django.contrib import admin

from .models import Group, Destination, Criteria, Navigation

# Register your models here.
admin.site.register(Group)
admin.site.register(Destination)
admin.site.register(Criteria)
admin.site.register(Navigation)
