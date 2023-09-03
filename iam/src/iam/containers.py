from dependency_injector import containers, providers
from microservice_utils.google_cloud.adapters.pubsub import Publisher, Subscriber


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    pubsub_publisher = providers.Factory(
        Publisher, config.GCP_PROJECT_ID, prepend_value=config.GCP_NAMESPACE
    )
    pubsub_subscriber = providers.Factory(
        Subscriber, config.GCP_PROJECT_ID, prepend_value=config.GCP_NAMESPACE
    )
