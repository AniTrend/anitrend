from django.contrib import admin
from .models import Series, Synonym, Source, Tag, Relation

# Register your models here.
admin.site.register(Series)
admin.site.register(Synonym)
admin.site.register(Source)
admin.site.register(Relation)
admin.site.register(Tag)
