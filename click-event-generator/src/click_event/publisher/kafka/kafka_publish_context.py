from json import dumps

DEFAULT_BROKER_ADDRESS = ['localhost:9091']
DEFAULT_CLICK_EVENT_TOPIC = "click-stream"
import base64

def get_click_event_topic():
    return DEFAULT_CLICK_EVENT_TOPIC


def get_kafka_broker_servers():
    return ['localhost:9091']


def get_default_value_serializer():
    return lambda x: base64.b64encode(dumps(x).encode('utf-8'))
