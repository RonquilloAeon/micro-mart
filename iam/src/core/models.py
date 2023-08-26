from cuid2 import Cuid
from django.db import models

CUID_GENERATOR: Cuid = Cuid(length=12)


class CuidField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 12
        kwargs["default"] = CUID_GENERATOR.generate
        kwargs["editable"] = False
        kwargs["unique"] = True
        super().__init__(*args, **kwargs)


class BaseModel(models.Model):
    id = CuidField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]
