from decimal import Decimal

from django.test import TestCase
from faker import Faker
from strawberry.relay.utils import to_base64

from core.models import CUID_GENERATOR
from core.testing import DependencyOverrideMixin, GraphQlMixin
from product.models import Product


class TestProductSchema(TestCase, DependencyOverrideMixin, GraphQlMixin):
    def setUp(self):
        self.faker = Faker()

    def _add_product(self, product_info: dict):
        # Add a product
        return self.query(
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
            mutation ($input: ProductAddInput!) {
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
            mutation ($input: ProductAddInput!) {
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

        self.assertTrue(result.data["productAddToCategory"]["success"])

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
            mutation ($input: ProductAddInput!) {
                productRemoveFromCategory(input: $input) {
                    entities {
                        id
                    }
                    success
                }
            }
            """,
            variables={"input": {"category": category_id, "product": product_id}},
        )

        self.assertTrue(result.data["productRemoveFromCategory"]["success"])

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
