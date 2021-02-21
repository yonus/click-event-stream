from abc import ABC,abstractmethod


class ClickEventReader:

    @abstractmethod
    def read(self):
        pass
