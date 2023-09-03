from uuid import UUID

from django.db.models import BooleanField, EmailField, TextField, UUIDField
from phonenumber_field.modelfields import PhoneNumberField

from core.models import BaseManager, BaseModel


class Manager(BaseManager):
    def register(
        self,
        first_name: str,
        last_name: str,
        remote_id: UUID,
        email: str = None,
        phone_number: str = None,
    ) -> "Member":
        if not email and not phone_number:
            raise ValueError("Either email or phone number must be provided.")

        member = Member(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            remote_id=remote_id,
        )
        member.save()

        return member


class Member(BaseModel):
    email = EmailField(null=True)
    first_name = TextField()
    last_name = TextField()
    is_active = BooleanField(default=True)
    phone_number = PhoneNumberField(null=True, region="US")
    remote_id = UUIDField(unique=True, editable=False)

    objects = Manager()

    def deactivate(self):
        self.is_active = False

        self.save(update_fields=["is_active"])
