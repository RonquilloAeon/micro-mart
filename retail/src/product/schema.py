import typing
from decimal import Decimal

import strawberry
import strawberry_django
from strawberry import relay

from core.graphql import MutationResult, convert_service_result_to_mutation_result
from product import models as product_models
from product.services import (
    AddCategoryService,
    AddProductService,
    AddProductToCategoriesService,
    CategoryData,
    ProductCategoriesData,
    ProductData,
    RemoveProductFromCategoriesService,
)


@strawberry_django.type(product_models.Category)
class Category(relay.Node):
    id: relay.NodeID[str]
    description: str
    name: str
    slug: str


@strawberry.input
class CategoryAddInput:
    description: str
    name: str
    slug: typing.Optional[str] = None


@strawberry_django.type(product_models.Product)
class Product(relay.Node):
    id: relay.NodeID[str]
    categories: list[Category]
    description: str
    name: str
    price: Decimal
    seller: str
    slug: str


@strawberry.input
class ProductAddInput:
    description: str
    name: str
    price: Decimal
    seller: str
    slug: typing.Optional[str] = None


@strawberry.input
class ProductCategoriesInput:
    categories: list[relay.GlobalID]
    product: relay.GlobalID


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def categoryAdd(self, info, input: CategoryAddInput) -> MutationResult:
        dto = CategoryData(
            description=input.description,
            name=input.name,
            slug=input.slug,
        )

        result = await AddCategoryService()(dto)

        return convert_service_result_to_mutation_result(result)

    @strawberry.mutation
    async def productAdd(self, info, input: ProductAddInput) -> MutationResult:
        dto = ProductData(
            description=input.description,
            name=input.name,
            price=input.price,
            seller=input.seller,
            slug=input.slug,
        )

        result = await AddProductService()(dto)

        return convert_service_result_to_mutation_result(result)

    @strawberry.mutation
    async def productAddToCategories(
        self, info, input: ProductCategoriesInput
    ) -> MutationResult:
        dto = ProductCategoriesData(
            categories=[c.node_id for c in input.categories],
            product=input.product.node_id,
        )

        result = await AddProductToCategoriesService()(dto)

        return convert_service_result_to_mutation_result(result)

    @strawberry.mutation
    async def productRemoveFromCategories(
        self, info, input: ProductCategoriesInput
    ) -> MutationResult:
        dto = ProductCategoriesData(
            categories=[c.node_id for c in input.categories],
            product=input.product.node_id,
        )

        result = await RemoveProductFromCategoriesService()(dto)

        return convert_service_result_to_mutation_result(result)


@strawberry.type
class Query:
    product: Product = relay.node()
    products: relay.ListConnection[Product] = strawberry.django.connection()
