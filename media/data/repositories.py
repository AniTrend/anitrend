from json import JSONDecodeError
from typing import cast

from uplink import HeaderMap
from core.repositories import DataRepository
from media.data.schemas import MediaApiResponse, MediaEntity
from media.data.sources import RemoteSource


class Repository(DataRepository):
    _remote_source: RemoteSource

    def invoke(self, **kwargs) -> MediaEntity:
        headers_value = kwargs.get("headers") or {}
        headers = cast(HeaderMap, headers_value)
        series_id_value = kwargs.get("series_id")
        if series_id_value is None:
            raise ValueError("series_id is required")
        series_id = int(series_id_value)
        try:
            response: MediaApiResponse = self._remote_source.get_series_by_id(
                series_id=series_id, headers=headers  # type: ignore[arg-type]
            )
            if not response.data:
                self._logger.error(
                    f"No data found for series_id {series_id}. Response: {response}"
                )
                raise ValueError(f"No data found for series_id {series_id}")
            if not isinstance(response.data, MediaEntity):
                self._logger.error(
                    f"Expected MediaEntity type but got {type(response.data)} for series_id {series_id}"
                )
                raise TypeError(
                    f"Expected MediaEntity type but got {type(response.data)} for series_id {series_id}"
                )
            self._logger.info(f"Successfully fetched series_id {series_id}")
            # Assuming response.data is of type Media
            return response.data
        except JSONDecodeError as e:
            self._logger.error(
                f"Malformed response while fetching series_id {series_id} with error message `{e.doc}`",
                exc_info=e,
            )
            raise e
        except Exception as e:
            self._logger.error(
                f"An unexpected error occurred while fetching series_id {series_id}",
                exc_info=e,
            )
            raise e
