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
        identifiers = {
            "anilist": kwargs.get("anilist"),
            "mal": kwargs.get("mal"),
            "trakt": kwargs.get("trakt"),
            "slug": kwargs.get("slug"),
            "tvdb": kwargs.get("tvdb"),
            "tmdb": kwargs.get("tmdb"),
            "notify": kwargs.get("notify"),
        }

        series_id = kwargs.get("series_id")
        if series_id is None and all(value is None for value in identifiers.values()):
            raise ValueError(
                "At least one identifier is required (anilist, mal, trakt, slug, tvdb, tmdb, notify)"
            )

        try:
            if series_id is not None:
                response: MediaApiResponse = self._remote_source.get_series_by_id(  # type: ignore[arg-type]
                    series_id=series_id, headers=headers
                )
            else:
                response = self._remote_source.get_series_by_id(  # type: ignore[arg-type]
                    headers=headers,
                    anilist=identifiers["anilist"],
                    mal=identifiers["mal"],
                    trakt=identifiers["trakt"],
                    slug=identifiers["slug"],
                    tvdb=identifiers["tvdb"],
                    tmdb=identifiers["tmdb"],
                    notify=identifiers["notify"],
                )

            if not response.data:
                message = (
                    f"No data found for series_id {series_id}"
                    if series_id is not None
                    else "No data found for supplied identifiers"
                )
                self._logger.error(message)
                raise ValueError(message)

            if not isinstance(response.data, MediaEntity):
                if series_id is not None:
                    error_message = f"Expected MediaEntity type but got {type(response.data)} for series_id {series_id}"
                else:
                    error_message = f"Expected MediaEntity type but got {type(response.data)} for identifiers {identifiers}"
                self._logger.error(error_message)
                raise TypeError(error_message)

            self._logger.info("Successfully fetched media entity")
            return response.data
        except JSONDecodeError as e:
            self._logger.error(
                f"Malformed response while fetching media with error message `{e.doc}`",
                exc_info=e,
            )
            raise e
        except Exception as e:
            if series_id is not None:
                self._logger.error(
                    f"An unexpected error occurred while fetching series_id {series_id}",
                    exc_info=e,
                )
            else:
                self._logger.error(
                    "An unexpected error occurred while fetching media entity",
                    exc_info=e,
                )
            raise e
