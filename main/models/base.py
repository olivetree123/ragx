import uuid

from django.db.models import (
    Model,
    AutoField,
    CharField,
    BooleanField,
    DateTimeField,
)
from django.utils import timezone
from django.forms.models import model_to_dict


def get_uid():
    return uuid.uuid4().hex


class BaseModel(Model):
    _id = AutoField(primary_key=True)
    id = CharField(max_length=32, unique=True, db_index=True, default=get_uid)
    created_at = DateTimeField(auto_now_add=timezone.now)
    updated_at = DateTimeField(auto_now=timezone.now)
    is_deleted = BooleanField(default=False)

    class Meta:
        abstract = True

    @classmethod
    def get_by_id(cls, id):
        return cls.objects.filter(id=id).first()

    def json(self, exclude=None):
        exclude_fields = ["_id", "is_deleted"]
        if exclude:
            exclude_fields.extend(exclude)
        return model_to_dict(self, exclude=exclude_fields)
