from json import JSONDecodeError
from typing import cast

from uplink import HeaderMap
from core.repositories import DataRepository
from media.data.schemas import MediaEntity
from media.data.sources import RemoteSource


class Repository(DataRepository):
    _remote_source: RemoteSource

    def invoke(self, **kwargs) -> MediaEntity:
        headers_value = kwargs.get("headers") or {}
        headers = cast(HeaderMap, headers_value)
        anilist_id_value = kwargs.get("anilist") or kwargs.get("series_id")
        if anilist_id_value is None:
            raise ValueError("anilist id is required")
        anilist_id = int(anilist_id_value)
        try:
            response: MediaEntity = self._remote_source.get_series(
                headers=headers,
                anilist=anilist_id,
                trakt=kwargs.get("trakt"),
                tvdb=kwargs.get("tvdb"),
                tmdb=kwargs.get("tmdb"),
                mal=kwargs.get("mal"),
                notify=kwargs.get("notify"),
                slug=kwargs.get("slug"),
            )
            if not response:
                self._logger.error(
                    f"No data found for anilist id {anilist_id}. Response: {response}"
                )
                raise ValueError(f"No data found for anilist id {anilist_id}")
            if not isinstance(response, MediaEntity):
                self._logger.error(
                    f"Expected MediaEntity type but got {type(response)} for anilist id {anilist_id}"
                )
                raise TypeError(
                    f"Expected MediaEntity type but got {type(response)} for anilist id {anilist_id}"
                )
            self._logger.info(f"Successfully fetched anilist id {anilist_id}")
            return response
        except JSONDecodeError as e:
            self._logger.error(
                f"Malformed response while fetching anilist id {anilist_id} with error message `{e.doc}`",
                exc_info=e,
            )
            raise e
        except Exception as e:
            self._logger.error(
                f"An unexpected error occurred while fetching anilist id {anilist_id}",
                exc_info=e,
            )
            raise e
