STATUS_CHOICES = (
    ("FINISHED", "FINISHED"),
    ("CURRENTLY", "CURRENTLY"),
    ("UPCOMING", "UPCOMING"),
    ("UNKNOWN", "UNKNOWN"),
)

TYPE_CHOICES = (
    ("TV", "TV"),
    ("Movie", "Movie"),
    ("OVA", "OVA"),
    ("ONA", "ONA"),
    ("Special", "Special")
)

SEASON_CHOICES = (
    ("WINTER", "WINTER"),
    ("SPRING", "SPRING"),
    ("SUMMER", "SUMMER"),
    ("FALL", "FALL"),
)


class AttributeDictionary(dict):
    """A dict that supports attribute access."""

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value
