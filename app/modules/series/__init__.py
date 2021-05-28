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
    RELEASING = "RELEASING"
    NOT_YET_RELEASED = "NOT_YET_RELEASED"

    CHOICES = [
        (FINISHED, "Finished airing"),
        (RELEASING, "Currently airing"),
        (NOT_YET_RELEASED, "Not yet released"),
    ]
