import time
import typing

from kafka import KafkaConsumer, KafkaProducer
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


class EventConsumer:
    def __init__(self, brokers: list[str], group_id: str, topic_namespace: str):
        self._brokers = brokers
        self._group_id = group_id
        self._topic_namespace = topic_namespace

    def events(self, topic) -> typing.Generator[EventEnvelope, None, None]:
        try:
            consumer = KafkaConsumer(
                f"{self._topic_namespace}.{topic}",
                bootstrap_servers=self._brokers,
                group_id=self._group_id,
                value_deserializer=lambda m: EventEnvelope.from_published_json(
                    m, allow_unregistered_events=True
                ),
            )

            for event in consumer:
                yield event.value
        except Exception:
            # TODO add logging
            time.sleep(5)

    def close(self):
        self.consumer.close()
