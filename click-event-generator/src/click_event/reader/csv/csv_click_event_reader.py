from datetime import datetime
from encodings.punycode import selective_find
from pathlib import Path
import  numpy as np
import pandas as pd

from click_event.model.click_event import ClickEvent

DEFAULT_CSV_PREFIX = "*.csv"

from click_event.reader.click_event_reader import ClickEventReader


class CsvClickEventReader(ClickEventReader):

    def __init__(self, file_directory, file_prefix=None):
        self._file_directory = file_directory
        self._file_prefix = file_prefix

    def read(self):
        return self.__read_generator()

    def __read_generator(self):
        base_path = self.__get_base_path()
        for csv_file in base_path.glob(self.__get_prefix()):
            df = pd.read_csv(csv_file, index_col=None, header=0)
            for k, row in df.iterrows():
                yield self.__convert_row_to_click_event(row)

    def __convert_row_to_click_event(self,row):

        click_event = ClickEvent()
        click_event.user_id = self.convert_data_type(row["user_id"])
        click_event.session_id = self.convert_data_type(row["session_id"])
        click_event.session_start = self.convert_data_type(row["session_start"])
        click_event.click_article_id = self.convert_data_type(row["click_article_id"])
        click_event.click_timestamp =  self.convert_data_type(row["click_timestamp"])
        click_event.click_environment = self.convert_data_type(row["click_environment"])
        click_event.click_device_group = self.convert_data_type(row["click_deviceGroup"])
        click_event.click_os = self.convert_data_type(row["click_os"])
        click_event.click_country = self.convert_data_type(row["click_country"])
        return click_event

    def convert_data_type(self,obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, datetime.datetime):
            return obj.__str__()
        else:
            return obj.__str__()

    def __get_base_path(self):
        return Path(self._file_directory)

    def __get_prefix(self):
        if self._file_prefix:
            return self._file_prefix

        return DEFAULT_CSV_PREFIX
