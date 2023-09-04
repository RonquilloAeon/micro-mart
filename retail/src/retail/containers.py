from dependency_injector import containers, providers

from adapters.streaming import EventConsumer, EventProducer
from adapters.typesense import TypesenseSearch


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    event_consumer = providers.Factory(
        EventConsumer,
        brokers=config.MESSAGING_BROKERS,
        group_id=config.SERVICE_NAME,
        topic_namespace=config.SERVICE_NAME,
    )
    event_producer = providers.Singleton(
        EventProducer,
        brokers=config.MESSAGING_BROKERS,
        topic_namespace=config.SERVICE_NAME,
    )

    search = providers.Factory(
        TypesenseSearch,
        config.SEARCH_API_KEY,
        host=config.SEARCH_HOST,
        port=config.SEARCH_PORT,
    )
