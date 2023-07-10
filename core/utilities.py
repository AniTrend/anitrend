import logging
from datetime import datetime, tzinfo
from typing import Optional, List
from urllib.parse import urlparse

import pytz


class LinkUtility:

    @staticmethod
    def extract_id_if_matches(urls: List[str], domain_name: str) -> Optional[str]:
        for url in urls:
            url_parse = urlparse(url)
            if url_parse.hostname == domain_name:
                return url_parse.path.split("/")[-1]
        return None


class TimeUtility:
    TIME_FORMAT_TEMPLATE = '%Y-%m-%dT%H:%M:%S%z'

    _logger = logging.getLogger('django')

    def __init__(self, time_zone) -> None:
        super().__init__()
        self._time_zone = time_zone

    def __get_current_tz(self) -> tzinfo:
        timezone = self._time_zone
        return pytz.timezone(timezone)

    def as_local_time(self, time_unit: str, time_unit_format: str = TIME_FORMAT_TEMPLATE) -> datetime:
        tz = self.__get_current_tz()
        current_time_unit = datetime.strptime(time_unit, time_unit_format)
        local_time = current_time_unit.astimezone(tz)
        self._logger.debug(
            f'Converted `{time_unit}` to local time of `{local_time}` using time format: `{time_unit_format}`'
        )
        return local_time

    def get_current_time_formatted(self, time_format: str = TIME_FORMAT_TEMPLATE) -> str:
        current_time = datetime.now(tz=self.__get_current_tz())
        return current_time.strftime(time_format)

    def get_current_time(self) -> datetime:
        current_time = datetime.now(tz=self.__get_current_tz())
        return current_time

    @staticmethod
    def from_date_time_to_time_stamp(time_unit: datetime) -> int:
        return int(time_unit.timestamp())

    def get_current_timestamp(self) -> int:
        current_date_time = self.get_current_time()
        current_time_stamp = self.from_date_time_to_time_stamp(current_date_time)
        return current_time_stamp
