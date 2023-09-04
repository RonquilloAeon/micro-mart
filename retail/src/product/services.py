import typing
from dataclasses import dataclass
from decimal import Decimal

from asgiref.sync import sync_to_async

from core.services import ServiceResult, execute_safely
from product.models import Category, Product


@dataclass
class CategoryData:
    description: str
    name: str
    slug: typing.Optional[str] = None


class AddCategoryService:
    @execute_safely
    async def __call__(self, data: CategoryData) -> ServiceResult:
        result = ServiceResult()

        category = await sync_to_async(self._add_category)(data)
        result.add_entity(category)

        return result

    def _add_category(self, data: CategoryData) -> Category:
        return Category.objects.add(
            description=data.description,
            name=data.name,
            slug=data.slug or None,
        )


@dataclass
class ProductData:
    description: str
    name: str
    price: typing.Union[Decimal, str]
    seller: str
    slug: typing.Optional[str] = None


class AddProductService:
    @execute_safely
    async def __call__(self, data: ProductData) -> ServiceResult:
        result = ServiceResult()

        product = await sync_to_async(self._add_product)(data)
        result.add_entity(product)

        return result

    def _add_product(self, data: ProductData) -> Product:
        price = Decimal(data.price)

        return Product.objects.add(
            description=data.description,
            name=data.name,
            price=price,
            seller=data.seller,
            slug=data.slug or None,
        )


@dataclass
class ProductCategoriesData:
    categories: list[str]
    product: str


class AddProductToCategoriesService:
    @execute_safely
    async def __call__(self, data: ProductCategoriesData) -> ServiceResult:
        result = ServiceResult()

        await sync_to_async(self._add_product_to_categories)(data)

        return result

    def _add_product_to_categories(self, data: ProductCategoriesData):
        categories = Category.objects.filter(id__in=data.categories)
        product = Product.objects.get(id=data.product)

        product.add_to_categories(*categories)


class RemoveProductFromCategoriesService:
    @execute_safely
    async def __call__(self, data: ProductCategoriesData) -> ServiceResult:
        result = ServiceResult()

        await sync_to_async(self._remove_product_from_categories)(data)

        return result

    def _remove_product_from_categories(self, data: ProductCategoriesData):
        categories = Category.objects.filter(id__in=data.categories)
        product = Product.objects.get(id=data.product)

        product.remove_from_categories(*categories)
