import pytest
import marshmallow
import serde
import serde.fields

from core.decorators import to_model
from core.schemas import CommonSchema

class TestModel(serde.Model):
    name = serde.fields.Str()
    value = serde.fields.Int()

@to_model(TestModel)
class TestSchema(CommonSchema):
    name = marshmallow.fields.String(required=True)
    value = marshmallow.fields.Integer(required=True)


class TestDecorator:
    def test_successful_conversion(self):
        test_data = {"name": "test", "value": 123}
        schema = TestSchema()

        result = schema.load(test_data)

        assert isinstance(result, TestModel)
        assert result.name == "test"
        assert result.value == 123

    def test_failed_conversion(self):
        test_data = {"name": "test"}
        schema = TestSchema()

        with pytest.raises(Exception):
            schema.load(test_data)

    def test_multiple_schema_instances(self):
        test_data = {"name": "test", "value": 123}
        schema1 = TestSchema()
        schema2 = TestSchema()

        result1 = schema1.load(test_data)
        result2 = schema2.load(test_data)

        assert isinstance(result1, TestModel)
        assert isinstance(result2, TestModel)
        assert result1.name == result2.name
        assert result1.value == result2.value
    
    def test_successful_conversion_with_json(self):
        test_data = '{"name": "test", "value": 123}'
        schema = TestSchema()

        result = schema.loads(test_data)

        assert isinstance(result, TestModel)
        assert result.name == "test"
        assert result.value == 123