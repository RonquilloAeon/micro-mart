from decimal import Decimal
from unittest.mock import call

from django.test import TestCase
from faker import Faker
from strawberry.relay.utils import to_base64

from core.models import CUID_GENERATOR
from core.testing import DependencyOverrideMixin, GraphQlMixin
from product import constants, events
from product.models import Product


class TestProductSchema(TestCase, DependencyOverrideMixin, GraphQlMixin):
    def setUp(self):
        self.faker = Faker()
        self.mock_dependencies()

    def _add_product(self, product_info: dict):
        # Add a product
        result = self.query(
            """
            mutation ($input: ProductAddInput!) {
                productAdd(input: $input) {
                    entities {
                        id
                        name
                        data
                    }
                    errors {
                        message
                    }
                    success
                }
            }
            """,
            variables={"input": product_info},
        )

        # Event check
        product = Product.objects.last()

        expected_event = events.ProductAdded(
            id=product.id, description=product.description, product_name=product.name
        )
        calls = [
            call(
                constants.EXTERNAL_TOPIC_NAME,
                expected_event,
            )
        ]
        self.mocks["event_producer"].publish.assert_has_calls(calls)

        self.reset_dependencies()

        return result

    def test_add_and_query(self):
        product_info = {
            "description": "The best headphones ever.",
            "name": "Sennheiser HD 800 S Headphones",
            "price": Decimal(999.99),
            "seller": CUID_GENERATOR.generate(),
        }
        result = self._add_product(product_info)

        product = Product.objects.last()
        product_id = to_base64("Product", product.id)

        expected_result = {
            "productAdd": {
                "entities": [{"id": product_id, "name": "Product", "data": {}}],
                "errors": [],
                "success": True,
            }
        }

        self.assertEqual(result.data, expected_result)

        # Query for the product
        result = self.query(
            """
            query ($id: GlobalID!) {
                product(id: $id) {
                    id
                    description
                    name
                    price
                    seller
                    slug
                }
            }
            """,
            variables={"id": product_id},
        )

        product_info["price"] = format(product_info["price"], ".2f")

        expected_result = {
            "product": {
                "id": product_id,
                **product_info,
                "slug": Product.to_slug(product_info["name"]),
            }
        }

        self.assertEqual(result.data, expected_result)

    def test_product_category(self):
        product_info = {
            "description": "The best headphones ever. Really.",
            "name": "Sennheiser HD 800 S Headphones",
            "price": Decimal(1999.99),
            "seller": CUID_GENERATOR.generate(),
        }
        self._add_product(product_info)

        product = Product.objects.last()
        product_id = to_base64("Product", product.id)

        # Add category
        category_info = {
            "description": "Personal electronics and more.",
            "name": "Electronics",
        }

        result = self.query(
            """
            mutation ($input: CategoryAddInput!) {
                categoryAdd(input: $input) {
                    entities {
                        id
                    }
                    success
                }
            }
            """,
            variables={"input": category_info},
        )

        category_id = result.data["categoryAdd"]["entities"][0]["id"]

        self.assertTrue(result.data["categoryAdd"]["success"])

        # Add product to category
        result = self.query(
            """
            mutation ($input: ProductCategoriesInput!) {
                productAddToCategories(input: $input) {
                    entities {
                        id
                    }
                    success
                }
            }
            """,
            variables={"input": {"categories": [category_id], "product": product_id}},
        )

        self.assertTrue(result.data["productAddToCategories"]["success"])

        # Query for the product
        result = self.query(
            """
            query ($id: GlobalID!) {
                product(id: $id) {
                    id
                    categories {
                        name
                    }
                    description
                    name
                    price
                    seller
                    slug
                }
            }
            """,
            variables={"id": product_id},
        )

        product_info["price"] = format(product_info["price"], ".2f")

        expected_result = {
            "product": {
                "id": product_id,
                "categories": [{"name": "Electronics"}],
                **product_info,
                "slug": Product.to_slug(product_info["name"]),
            }
        }

        self.assertEqual(result.data, expected_result)

        # Remove category
        result = self.query(
            """
            mutation ($input: ProductCategoriesInput!) {
                productRemoveFromCategories(input: $input) {
                    entities {
                        id
                    }
                    success
                }
            }
            """,
            variables={"input": {"categories": [category_id], "product": product_id}},
        )

        self.assertTrue(result.data["productRemoveFromCategories"]["success"])

        # Query product again. This time, we don't expect any categories
        result = self.query(
            """
            query ($id: GlobalID!) {
                product(id: $id) {
                    categories {
                        name
                    }
                }
            }
            """,
            variables={"id": product_id},
        )

        expected_result = {
            "product": {
                "categories": [],
            }
        }

        self.assertEqual(result.data, expected_result)
