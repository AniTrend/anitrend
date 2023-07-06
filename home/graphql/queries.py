from typing import Dict

from graphene import ObjectType, Field
from graphql import GraphQLResolveInfo

from .types import HomeObjectType


class HomeQuery(ObjectType):
    home = Field(
        HomeObjectType,
        name="home",
        description="Home entries",
    )

    @staticmethod
    def resolve_home(root, info: GraphQLResolveInfo, **kwargs) -> Dict:
        # Querying a list
        return {
            'genres': [
                {
                    "genre": "Action",
                    "mediaId": 101922,
                    "image": "https://img.anili.st/media/101922"
                },
                {
                    "genre": "Adventure",
                    "mediaId": 108465,
                    "image": "https://img.anili.st/media/108465"
                },
                {
                    "genre": "Comedy",
                    "mediaId": 21087,
                    "image": "https://img.anili.st/media/21087"
                },
                {
                    "genre": "Drama",
                    "mediaId": 20605,
                    "image": "https://img.anili.st/media/20605"
                },
                {
                    "genre": "Ecchi",
                    "mediaId": 20923,
                    "image": "https://img.anili.st/media/20923"
                },
                {
                    "genre": "Fantasy",
                    "mediaId": 101759,
                    "image": "https://img.anili.st/media/101759"
                },
                {
                    "genre": "Hentai",
                    "mediaId": 20807,
                    "image": "https://img.anili.st/media/20807"
                },
                {
                    "genre": "Horror",
                    "mediaId": 11111,
                    "image": "https://img.anili.st/media/11111"
                },
                {
                    "genre": "Mahou Shoujo",
                    "mediaId": 104051,
                    "image": "https://img.anili.st/media/104051"
                },
                {
                    "genre": "Mecha",
                    "mediaId": 99423,
                    "image": "https://img.anili.st/media/99423"
                },
                {
                    "genre": "Music",
                    "mediaId": 20665,
                    "image": "https://img.anili.st/media/20665"
                },
                {
                    "genre": "Mystery",
                    "mediaId": 1535,
                    "image": "https://img.anili.st/media/1535"
                },
                {
                    "genre": "Psychological",
                    "mediaId": 21355,
                    "image": "https://img.anili.st/media/21355"
                },
                {
                    "genre": "Romance",
                    "mediaId": 21519,
                    "image": "https://img.anili.st/media/21519"
                },
                {
                    "genre": "Sci-Fi",
                    "mediaId": 6880,
                    "image": "https://img.anili.st/media/6880"
                },
                {
                    "genre": "Slice of Life",
                    "mediaId": 21827,
                    "image": "https://img.anili.st/media/21827"
                },
                {
                    "genre": "Sports",
                    "mediaId": 20464,
                    "image": "https://img.anili.st/media/20464"
                },
                {
                    "genre": "Supernatural",
                    "mediaId": 21234,
                    "image": "https://img.anili.st/media/21234"
                },
                {
                    "genre": "Thriller",
                    "mediaId": 129201,
                    "image": "https://img.anili.st/media/129201"
                }
            ]
        }
