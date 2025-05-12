import strawberry


@strawberry.type
class MediaQuery:
    @strawberry.field
    def hello_media(self) -> str:
        return "Hi from media!"
