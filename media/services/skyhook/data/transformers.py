from typing import List, Optional, Dict

from media.models import Season
from ..domain.entities import SkyhookImage


class Transformer:

    @staticmethod
    def __get_image_by_type(images: List[SkyhookImage], image_type: str) -> Optional[str]:
        for image in images:
            if image.coverType == image_type:
                return image.url
        return None

    @staticmethod
    def __get_season_by_number(season_map: Dict, season_number: int) -> Optional[Season]:
        season_number_key = f"{season_number}"
        if season_number_key in season_map:
            return season_map[season_number_key]
        return None
