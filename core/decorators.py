import logging
from typing import Dict, Type
from serde import Model
from uplink import error_handler

from core.schemas import CommonSchema


@error_handler(requires_consumer=True)
def raise_api_error(consumer, exc_type=None, exc_val=None, exc_tb=None):
    logger = logging.getLogger("django")
    logger.warning(
        f"API error occurred -> exc_type: {exc_type} exc_val: {exc_val} exc_tb: {exc_tb}"
    )


def to_model(model_class: Type[Model]):
    """
    Decorator that adds functionality to schema classes to convert dict to model instance.

    Args:
        model_class: The model class to convert the dictionary data into
    """

    def decorator(schema_class: CommonSchema):
        def on_post_serialization(
            self: CommonSchema, data: Dict, many: bool, **kwargs
        ) -> Model:
            self._logger.debug(f"Executing post_load for {model_class.__name__}")
            try:
                model = model_class.from_dict(data)
                return model
            except Exception as e:
                self._logger.error(f"Conversion from dictionary failed", exc_info=e)
                raise e

        schema_class._on_post_load = on_post_serialization
        return schema_class

    return decorator
