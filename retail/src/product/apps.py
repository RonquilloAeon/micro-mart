from django.apps import AppConfig

from retail import container


class ProductConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "product"

    def ready(self):
        container.wire(
            modules=[
                ".event_handlers",
                ".management.commands.sync_product_search",
                ".services",
            ]
        )
