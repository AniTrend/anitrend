import json
import logging
from logging import Logger
from typing import Any, Optional, Dict, Union, cast

from marshmallow import Schema, post_load
from marshmallow.schema import SchemaMeta
from marshmallow.types import StrSequenceOrSet
from serde import Model


class CommonSchema(Schema):
    _logger: Logger = logging.getLogger("django")

    @post_load()
    def _on_post_load(self, data: Dict, many: bool, **kwargs) -> Model:
        pass
