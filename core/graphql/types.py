import strawberry


class Instant(int):
    """Epoch timestamp in seconds since Unix epoch."""


# Register the GraphQL scalar for the Instant type
InstantScalar = strawberry.scalar(
    Instant,
    name="Instant",
    description="Represents a point in time, typically as an Epoch timestamp (seconds since Unix epoch).",
)
