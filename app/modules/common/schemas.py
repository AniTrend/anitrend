from logging import Logger
from typing import Any, Optional, Dict, Union

from marshmallow import Schema
from marshmallow.types import StrSequenceOrSet

from app.dependencies import AppContainer


class CommonSchema(Schema):
    _logger: Logger

    def __init__(self, *, only: Optional[StrSequenceOrSet] = None, exclude: StrSequenceOrSet = (),
                 many: bool = False, context: Optional[Dict] = None,
                 load_only: StrSequenceOrSet = (), dump_only: StrSequenceOrSet = (),
                 partial: Union[bool, StrSequenceOrSet] = False, unknown: Optional[str] = None):
        super().__init__(only=only, exclude=exclude, many=many, context=context, load_only=load_only,
                         dump_only=dump_only, partial=partial, unknown=unknown)
        self._logger = AppContainer.logging_utility().get_default_logger(__name__)

    def _on_post_load(self, data, many, **kwargs) -> Any:
        pass
