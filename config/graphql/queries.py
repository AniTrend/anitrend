import strawberry
from typing import Optional
from strawberry.types import Info

from .resolvers import resolve_config
from .types import Configuration


@strawberry.type
class ConfigQuery:

    @strawberry.field(description="Client configuration")
    def config(self, info: Info) -> Optional[Configuration]:
        return resolve_config(context = info.context)
