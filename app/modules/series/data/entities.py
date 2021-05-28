from dataclasses import dataclass
from typing import Optional, List


@dataclass
class SeriesParams:
    tvdb: Optional[int]
    anidb: Optional[int]
    anilist: Optional[int]
    animeplanet: Optional[str]
    notify: Optional[str]
    kitsu: Optional[int]
    mal: Optional[int]


@dataclass
class SeasonParams:
    seriesId: Optional[int]
