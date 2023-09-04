from dependency_injector import containers, providers

from adapters.streaming import EventProducer


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    event_producer = providers.Singleton(
        EventProducer, brokers=config.MESSAGING_BROKERS, topic_namespace=config.SERVICE_NAME
    )
