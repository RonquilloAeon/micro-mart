from django.db.models import ManyToManyField, TextChoices, TextField
from django_choices_field import TextChoicesField

from core.models import BaseModel


class Employee(BaseModel):
    teams = ManyToManyField("Team", related_name="employees")


class Team(BaseModel):
    class AreaEnum(TextChoices):
        BIZ_DEV = "biz_dev", "Business Development"
        DATA = "data", "Data Science"
        ENGINEERING = "engineering", "Engineering"
        FINANCE = "finance", "Finance"
        HR = "hr", "Human Resources"
        INVENTORY = "inventory", "Inventory Management"
        MARKETING = "marketing", "Marketing"
        SUPPLY_CHAIN = "supply_chain", "Supply Chain Management"
        SUPPORT = "support", "Customer Support"

    name = TextField()
    area = TextChoicesField(choices_enum=AreaEnum)
