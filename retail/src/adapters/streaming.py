from kafka import KafkaProducer
from microservice_utils.events import Event, EventEnvelope


class EventProducer:
    def __init__(self, brokers: list[str], topic_namespace: str):
        self._producer = KafkaProducer(
            bootstrap_servers=brokers,
            value_serializer=lambda v: v.to_publishable_json(),
        )
        self._topic_namespace = topic_namespace

    def publish(self, topic: str, event: Event):
        message = EventEnvelope.create(event)
        self._producer.send(f"{self._topic_namespace}.{topic}", message)

        self._producer.flush()

    def close(self):
        self._producer.close()
