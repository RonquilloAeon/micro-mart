from microservice_utils.events import Event


class ProductAdded(Event):
    id: str
    description: str
    product_name: str
