import pytest
from django.urls import reverse
from django.test import RequestFactory
from graphene.test import Client
from app.graphql import schema


def test_media_query():
    query = """
    """

    expected = {
        "data": {
            "media": {
                "node": {
                    "name": "Level R",
                    "brand": "Mondraker",
                    "year": "2020",
                    "size": ["S", "M", "L", "XL"],
                    "wheelSize": 27.5,
                    "type": "MTB",
                }
            }
        }
    }

    client = Client(schema)
    result = client.execute(query)
    assert result == expected
