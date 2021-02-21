import os

from click_event.publisher.kafka.kafka_click_event_publisher import KafkaClickEventPublisher
from click_event.reader.csv.csv_click_event_reader import CsvClickEventReader

CLICK_EVENT_FILE_DIRECTORY  = "CLICK_EVENT_FILE_DIRECTORY"

def get_click_event_file_directory():
     if os.getenv(CLICK_EVENT_FILE_DIRECTORY):
          return os.getenv(CLICK_EVENT_FILE_DIRECTORY)
     return "../data/clicks2"

if __name__ == '__main__':
    reader = CsvClickEventReader(get_click_event_file_directory())
    click_event_publisher = KafkaClickEventPublisher()
    for click_event in reader.read():
       print("event is {}".format(click_event.to_dict()))
       click_event_publisher.publish(click_event)




