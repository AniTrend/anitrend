from dataclasses import dataclass
from typing import Optional


@dataclass
class MediaParams:
    tvdb: Optional[int]
    anidb: Optional[int]
    anilist: Optional[int]
    animeplanet: Optional[str]
    notify: Optional[str]
    kitsu: Optional[int]
    mal: Optional[int]


@dataclass
class SeasonParams:
    mediaId: Optional[int]
