from click_event.model.click_event import ClickEvent
from click_event.publisher.click_event_publisher import ClickEventPublisher
from kafka import KafkaProducer

from click_event.publisher.kafka.kafka_publish_context import get_kafka_broker_servers, get_default_value_serializer, \
    get_click_event_topic


class KafkaClickEventPublisher(ClickEventPublisher):

    def __init__(self):
        self.__init_kafka_producer()
        self.__topic = get_click_event_topic()

    def publish(self, click_event: ClickEvent):
        self.__producer.send(self.__topic,click_event.to_dict())

    def __init_kafka_producer(self):
        self.__producer = KafkaProducer(bootstrap_servers=get_kafka_broker_servers(),value_serializer=get_default_value_serializer())


