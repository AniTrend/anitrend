from typing import List

from uplink import get, Query, Consumer

from core.decorators import retry_and_ratelimit_strategy, raise_api_error
from .schemas import ArmModelSchema


@retry_and_ratelimit_strategy
class ArmEndpoint(Consumer):

    @raise_api_error
    @get("api/v2/ids")
    def get_with_id(
            self,
            id: Query(name="id", type=str),
            source: Query(name="source", type=str) = "anilist"
    ) -> ArmModelSchema:
        pass

    @raise_api_error
    @get("api/v2/thetvdb")
    def get_ids_from_tvdb(
            self,
            id: Query(name="id", type=str)
    ) -> List[ArmModelSchema]:
        pass
