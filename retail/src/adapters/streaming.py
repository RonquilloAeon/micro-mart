from kafka import KafkaProducer
from microservice_utils.events import Event, EventEnvelope


class EventProducer:
    def __init__(self, brokers: list[str]):
        self.producer = KafkaProducer(
            bootstrap_servers=brokers,
            value_serializer=lambda v: v.to_publishable_json(),
        )

    def publish(self, topic: str, event: Event):
        message = EventEnvelope.create(event)
        self.producer.send(topic, message)

        self.producer.flush()

    def close(self):
        self.producer.close()
