from microservice_utils.events import Event


class ProductAdded(Event):
    id: str
    product_name: str
