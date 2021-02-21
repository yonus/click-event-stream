from abc import ABC, abstractmethod

from click_event.model.click_event import ClickEvent


class ClickEventPublisher(ABC):

    @abstractmethod
    def publish(self, click_event: ClickEvent):
        pass
