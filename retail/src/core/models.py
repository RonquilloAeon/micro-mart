from cuid2 import Cuid
from django.db import models

CUID_GENERATOR: Cuid = Cuid(length=12)


class CuidField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 12
        kwargs["default"] = CUID_GENERATOR.generate
        super().__init__(*args, **kwargs)


class BaseManager(models.Manager):
    """This manager discourages the use of typical Django factory methods
    in new models in favor of methods alignd with our ubiquitous language."""

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def create_or_update(self, *args, **kwargs):
        raise NotImplementedError


class BaseModel(models.Model):
    id = CuidField(editable=False, primary_key=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]
