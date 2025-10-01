from typing import Optional
import strawberry


class Instant(int):
    """Epoch timestamp in seconds since Unix epoch."""


# Register the GraphQL scalar for the Instant type
InstantScalar = strawberry.scalar(
    Instant,
    name="Instant",
    description="Represents a point in time, typically as an Epoch timestamp (seconds since Unix epoch).",
)


@strawberry.type
class EdgeImage:
    height: int = strawberry.field(description="Height of the image in pixels")
    width: int = strawberry.field(description="Width of the image in pixels")
    url: str = strawberry.field(description="URL to the image")
    type: str = strawberry.field(
        description="Type of the image (e.g., BACKDROP, LOGO, POSTER)"
    )
    locale: Optional[str] = strawberry.field(
        description="Locale of the image (e.g., en, ja)", default=None
    )
