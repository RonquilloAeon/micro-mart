import re
import typing
from decimal import Decimal

from django.db.models import (
    BooleanField,
    CASCADE,
    DecimalField,
    ForeignKey,
    ManyToManyField,
    TextField,
)

from core.models import BaseManager, BaseModel, CuidField


class SlugMixin:
    @staticmethod
    def to_slug(string: str) -> str:
        slug_str = string.lower()
        slug_str = re.sub(r"[^a-zA-Z0-9\s]", "", slug_str)
        return slug_str.replace(" ", "-")

    def update_slug(self, slug: str):
        self.slug = self.to_slug(slug)
        self.save(update_fields=["slug"])


class CategoryManager(BaseManager):
    def add(
        self,
        description: str,
        name: str,
        parent: typing.Optional["Category"] = None,
        slug: typing.Optional[str] = None,
    ):
        slug = Category.to_slug(slug or name)
        category = Category(
            description=description,
            name=name,
            slug=slug,
        )
        category.save()

        if parent:
            category.set_parent(parent)

        return category


class Category(BaseModel, SlugMixin):
    description = TextField()
    name = TextField()
    parent = ForeignKey("Category", on_delete=CASCADE, null=True)
    slug = TextField()

    objects = CategoryManager()

    def set_parent(self, parent: "Category"):
        self.parent = parent
        self.save(update_fields=["parent"])


class ProductManager(BaseManager):
    def add(
        self,
        description: str,
        name: str,
        price: Decimal,
        seller: str,
        slug: typing.Optional[str] = None,
    ) -> "Product":
        product = Product(
            description=description,
            name=name,
            price=price,
            seller=seller,
        )
        product.save()
        product.update_slug(slug or name)

        return product


class Product(BaseModel, SlugMixin):
    categories = ManyToManyField(
        to=Category,
        related_name="products",
    )
    description = TextField()
    is_available_for_purchase = BooleanField(default=True)
    name = TextField()
    price = DecimalField(max_digits=10, decimal_places=2)
    seller = CuidField(editable=True, unique=False)
    slug = TextField()

    objects = ProductManager()

    def add_to_categories(self, *categories: Category):
        self.categories.add(*categories)

    def remove_from_categories(self, *categories: Category):
        self.categories.remove(*categories)

    def update_price(self, new_price: Decimal):
        raise NotImplementedError


# TODO add seller model
