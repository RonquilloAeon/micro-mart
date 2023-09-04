from product import events


def update_typesense(event: events.ProductAdded):
    print("recv event", event)
