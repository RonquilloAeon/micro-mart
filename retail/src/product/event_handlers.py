from dependency_injector.wiring import inject, Provide
from strawberry.relay.utils import to_base64

from adapters.typesense import TypesenseSearch
from product import events, models
from retail.containers import Container


@inject
def update_typesense(
    event: events.ProductAdded,
    search: TypesenseSearch = Provide[Container.search],
):
    product = models.Product.objects.get(id=event.id)

    # TODO abstract this
    document = {
        "id": to_base64("Product", product.id),
        "categories": [cat.name for cat in product.categories.all()],
        "description": product.description,
        "name": product.name,
        "price": float(product.price),
        "seller": to_base64("Member", "product.seller"),  # TODO add seller model
        "slug": product.slug,
    }

    search.add("products", document)
