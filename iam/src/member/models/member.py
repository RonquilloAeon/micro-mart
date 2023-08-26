from django.db.models import EmailField, UUIDField
from phonenumber_field.modelfields import PhoneNumberField

from core.models import BaseModel


class Member(BaseModel):
    email = EmailField(null=True)
    phone_number = PhoneNumberField(null=True, region="US")
    remote_id = UUIDField(unique=True, editable=False)
