"""Series package"""


class SeasonTypes:
    WINTER = "WINTER"
    SPRING = "SPRING"
    SUMMER = "SUMMER"
    FALL = "FALL"

    CHOICES = [
        (WINTER, "Winter season"),
        (SPRING, "Spring season"),
        (SUMMER, "Summer season"),
        (FALL, "Fall season"),
    ]


class SeriesTypes:
    TV = "TV"
    Movie = "Movie"
    OVA = "OVA"
    ONA = "ONA"
    Special = "Special"

    CHOICES = [
        (TV, "TV"),
        (Movie, "Movie"),
        (OVA, "OVA"),
        (ONA, "ONA"),
        (Special, "Special"),
    ]


class StatusTypes:
    FINISHED = "FINISHED"
    CURRENTLY = "CURRENTLY"
    UPCOMING = "UPCOMING"
    UNKNOWN = "UNKNOWN"

    CHOICES = [
        (FINISHED, "Finished airing"),
        (CURRENTLY, "Currently airing"),
        (UPCOMING, "Not yet released"),
        (UNKNOWN, "Unknown status"),
    ]
