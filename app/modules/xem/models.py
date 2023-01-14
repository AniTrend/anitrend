from mongoengine import Document, ObjectIdField
from mongoengine.fields import (
    IntField,
    StringField,
    ListField,
    DateTimeField
)
from django.utils import timezone


class Xem(Document):
    ID = ObjectIdField()
    id = IntField(primary_key=True)
    titles = ListField(StringField(max_length=256))
    updated_at = DateTimeField(default=timezone.now().utcnow())

    def __str__(self):
        return f"{self.id} - {self.titles}"
