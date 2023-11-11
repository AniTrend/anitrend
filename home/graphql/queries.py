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
                    "name": "Action",
                    "mediaId": 101922,
                    "image": "https://img.anili.st/media/101922"
                },
                {
                    "name": "Adventure",
                    "mediaId": 108465,
                    "image": "https://img.anili.st/media/108465"
                },
                {
                    "name": "Comedy",
                    "mediaId": 21087,
                    "image": "https://img.anili.st/media/21087"
                },
                {
                    "name": "Drama",
                    "mediaId": 20605,
                    "image": "https://img.anili.st/media/20605"
                },
                {
                    "name": "Ecchi",
                    "mediaId": 20923,
                    "image": "https://img.anili.st/media/20923"
                },
                {
                    "name": "Fantasy",
                    "mediaId": 101759,
                    "image": "https://img.anili.st/media/101759"
                },
                {
                    "name": "Hentai",
                    "mediaId": 20807,
                    "image": "https://img.anili.st/media/20807"
                },
                {
                    "name": "Horror",
                    "mediaId": 11111,
                    "image": "https://img.anili.st/media/11111"
                },
                {
                    "name": "Mahou Shoujo",
                    "mediaId": 104051,
                    "image": "https://img.anili.st/media/104051"
                },
                {
                    "name": "Mecha",
                    "mediaId": 99423,
                    "image": "https://img.anili.st/media/99423"
                },
                {
                    "name": "Music",
                    "mediaId": 20665,
                    "image": "https://img.anili.st/media/20665"
                },
                {
                    "name": "Mystery",
                    "mediaId": 1535,
                    "image": "https://img.anili.st/media/1535"
                },
                {
                    "name": "Psychological",
                    "mediaId": 21355,
                    "image": "https://img.anili.st/media/21355"
                },
                {
                    "name": "Romance",
                    "mediaId": 21519,
                    "image": "https://img.anili.st/media/21519"
                },
                {
                    "name": "Sci-Fi",
                    "mediaId": 6880,
                    "image": "https://img.anili.st/media/6880"
                },
                {
                    "name": "Slice of Life",
                    "mediaId": 21827,
                    "image": "https://img.anili.st/media/21827"
                },
                {
                    "name": "Sports",
                    "mediaId": 20464,
                    "image": "https://img.anili.st/media/20464"
                },
                {
                    "name": "Supernatural",
                    "mediaId": 21234,
                    "image": "https://img.anili.st/media/21234"
                },
                {
                    "name": "Thriller",
                    "mediaId": 129201,
                    "image": "https://img.anili.st/media/129201"
                }
            ]
        }
