from dependency_injector.wiring import inject, Provide
from django.core.management import BaseCommand
from strawberry.relay.utils import to_base64

from adapters.typesense import TypesenseSearch
from product.models import Product
from retail.containers import Container


class Command(BaseCommand):
    help = "Update product search repository."

    @inject
    def handle(
        self,
        *args,
        search: TypesenseSearch = Provide[Container.search],
        **options,
    ):
        # TODO build programmatic schema generation and aliasing
        product_schema = {
            "name": "products",
            "fields": [
                {"name": "id", "type": "string"},  # GlobalID
                {"name": "categories", "type": "string[]", "facet": True},
                {"name": "description", "type": "string"},
                {"name": "name", "type": "string"},
                {"name": "price", "type": "float"},  # Decimal actually
                {"name": "seller", "type": "string"},
                {"name": "slug", "type": "string"},
            ],
        }

        collection_name = search.create_collection(product_schema)

        # Sync products
        product_documents = []

        for product in Product.objects.all().iterator(chunk_size=100):
            product_document = {
                "id": to_base64("Product", product.id),
                "categories": [cat.name for cat in product.categories.all()],
                "description": product.description,
                "name": product.name,
                "price": float(product.price),
                "seller": to_base64(
                    "Member", "product.seller"
                ),  # TODO add seller model
                "slug": product.slug,
            }
            product_documents.append(product_document)

            # Batch add
            if len(product_documents) == 100:
                search.batch_add(collection_name, product_documents)
                product_documents = []

        # Add any remaining product documents to the collection
        if product_documents:
            print("Adding", product_documents)
            search.batch_add(collection_name, product_documents)
