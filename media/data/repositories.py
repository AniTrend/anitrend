from json import JSONDecodeError
from uplink import HeaderMap
from ..data.schemas import Media, MediaApiResponse
from core.repositories import DataRepository
from ..data.sources import RemoteSource


class Repository(DataRepository):
    _remote_source: RemoteSource

    def get_series_by_id(self, series_id: int, **kwargs) -> Media:
        try:
            headers: HeaderMap = kwargs.get("headers")
            response: MediaApiResponse = self._remote_source.get_series_by_id(
                series_id=series_id, headers=headers
            )
            if not response.data:
                self._logger.error(
                    f"No data found for series_id {series_id}. Response: {response}"
                )
                raise ValueError(f"No data found for series_id {series_id}")
            if not isinstance(response.data, Media):
                self._logger.error(
                    f"Expected Media type but got {type(response.data)} for series_id {series_id}"
                )
                raise TypeError(
                    f"Expected Media type but got {type(response.data)} for series_id {series_id}"
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
