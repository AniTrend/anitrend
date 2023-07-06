from typing import Optional

from .models import Device
from ua_parser import user_agent_parser


class UAParser:
    def __init__(self, user_agent: Optional[str] = None):
        self.ua = user_agent_parser.Parse(user_agent or '')

    def get_result(self) -> Device:
        return Device(
            browser=self.ua.get('user_agent', {}).get('family'),
            cpu=self.ua('cpu', {}).get('architecture'),
            device=self.ua('device', {}).get('family'),
            engine=self.ua('user_agent', {}).get('family'),
            os=self.ua('os', {}).get('family'),
        )

