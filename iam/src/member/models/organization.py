from django.db.models import CASCADE, ForeignKey, ManyToManyField, TextField

from core.models import BaseModel


class Organization(BaseModel):
    members = ManyToManyField(
        "Member", related_name="organizations", through="OrganizationMember"
    )
    name = TextField()


class OrganizationMember(BaseModel):
    member = ForeignKey(
        "Member", on_delete=CASCADE, related_name="organization_memberships"
    )
    organization = ForeignKey(
        Organization,
        on_delete=CASCADE,
        related_name="organization_members",
    )
