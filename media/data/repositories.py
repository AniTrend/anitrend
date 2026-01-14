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
        identifiers = {
            "anilist": kwargs.get("anilist") or kwargs.get("series_id"),
            "trakt": kwargs.get("trakt"),
            "tvdb": kwargs.get("tvdb"),
            "tmdb": kwargs.get("tmdb"),
            "mal": kwargs.get("mal"),
            "notify": kwargs.get("notify"),
            "slug": kwargs.get("slug"),
        }

        if not any(identifiers.values()):
            raise ValueError(
                "At least one identifier (anilist/trakt/tvdb/tmdb/mal/notify/slug) is required"
            )

        # Normalize numeric identifiers to int where provided
        if identifiers["anilist"] is not None:
            identifiers["anilist"] = int(identifiers["anilist"])
        if identifiers["trakt"] is not None:
            identifiers["trakt"] = int(identifiers["trakt"])
        if identifiers["tvdb"] is not None:
            identifiers["tvdb"] = int(identifiers["tvdb"])
        if identifiers["tmdb"] is not None:
            identifiers["tmdb"] = int(identifiers["tmdb"])
        if identifiers["mal"] is not None:
            identifiers["mal"] = int(identifiers["mal"])
        try:
            response: MediaEntity = self._remote_source.get_series(
                headers=headers,
                **identifiers,
            )
            if not response:
                self._logger.error(
                    f"No data found for identifiers {identifiers}. Response: {response}"
                )
                raise ValueError("No data found for provided identifiers")
            if not isinstance(response, MediaEntity):
                self._logger.error(
                    f"Expected MediaEntity type but got {type(response)} for identifiers {identifiers}"
                )
                raise TypeError(
                    f"Expected MediaEntity type but got {type(response)} for provided identifiers"
                )
            self._logger.info(
                f"Successfully fetched media with identifiers {identifiers}"
            )
            return response
        except JSONDecodeError as e:
            self._logger.error(
                f"Malformed response while fetching identifiers {identifiers} with error message `{e.doc}`",
                exc_info=e,
            )
            raise e
        except Exception as e:
            self._logger.error(
                f"An unexpected error occurred while fetching identifiers {identifiers}",
                exc_info=e,
            )
            raise e
