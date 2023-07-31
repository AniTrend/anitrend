import json
import logging
from logging import Logger
from typing import Any, Optional, Dict, Union, cast

from marshmallow import Schema
from marshmallow.schema import SchemaMeta
from marshmallow.types import StrSequenceOrSet


class CommonSchema(Schema):
    _logger: Logger = logging.getLogger("django")

    def __init__(self, *, only: Optional[StrSequenceOrSet] = None, exclude: StrSequenceOrSet = (),
                 many: bool = False, context: Optional[Dict] = None,
                 load_only: StrSequenceOrSet = (), dump_only: StrSequenceOrSet = (),
                 partial: Union[bool, StrSequenceOrSet] = False, unknown: Optional[str] = None):
        super().__init__(only=only, exclude=exclude, many=many, context=context, load_only=load_only,
                         dump_only=dump_only, partial=partial, unknown=unknown)

    def _on_post_load(self, data, many, **kwargs) -> Any:
        pass

    def from_json(self, content: str) -> SchemaMeta:
        mapping = json.loads(content)
        return cast(SchemaMeta, self.from_dict(mapping))
