import django
from dependency_injector.wiring import inject, Provide
from microservice_utils.events import EventEnvelope

django.setup()

from adapters.streaming import EventConsumer  # noqa E402
from product import constants as product_constants  # noqa E402
from product import event_handlers as product_handlers  # noqa E402
from product import events as product_events  # noqa E402
from retail import settings  # noqa E402
from retail.containers import Container  # noqa E402

EVENT_HANDLERS = {
    product_events.ProductAdded.name: [product_handlers.update_typesense],
}


def _handle_event(envelope: EventEnvelope):
    handlers = EVENT_HANDLERS.get(envelope.event_type, [])

    for handler in handlers:
        handler(envelope.event)


@inject
def consume_events(
    event_consumer: EventConsumer = Provide[Container.event_consumer],
):
    # TODO enable subscribing to multiple topics
    for event in event_consumer.events(product_constants.EXTERNAL_TOPIC_NAME):
        _handle_event(event)


def main():
    container = Container()
    container.config.from_dict(settings.__dict__)
    container.wire(modules=[__name__])

    consume_events()


if __name__ == "__main__":
    main()
