from typing import Optional, Dict, Any, Mapping

from ua_parser import user_agent_parser

from .models import UserAgentInfo, UserAgent, CPU, Device, OS


def get_forwarded_headers(context) -> Optional[Mapping]:
    keys_to_pick = [
        'host',
        'accept',
        'accept-encoding',
        'accept-language',
        'user-agent',
        'content-type',
        'x-app-name',
        'x-app-version',
        'x-app-code',
        'x-app-source',
        'x-app-locale',
        'x-app-build-type'
    ]
    headers: Optional[Mapping] = None
    if hasattr(context, 'headers'):
        request_headers: Mapping = context.headers
        headers = {key: request_headers[key] for key in keys_to_pick if key in request_headers}
    return headers


def safe_get(dictionary: Dict[str, any], keys: str, default: Optional[any] = None) -> any:
    """
    Safely get a nested value from a dictionary.

    Args:
        dictionary (Dict[str, any]): The dictionary to extract the value from.
        keys (str): A string representing the keys separated by dots.
        default (Optional[any], optional): Default value to return if the keys are not found. Defaults to None.

    Returns:
        any: The value found at the specified keys, or the default value if not found.
    """
    keys_list = keys.split('.')
    for key in keys_list:
        if isinstance(dictionary, dict) and key in dictionary:
            dictionary = dictionary[key]
        else:
            return default if default is not None else {}
    return dictionary


class UAParser:
    def __init__(self, user_agent: Optional[str] = None):
        self.ua = user_agent_parser.Parse(user_agent or '')

    def get_result(self) -> UserAgentInfo:
        return UserAgentInfo(
            raw=safe_get(self.ua, 'string'),
            user_agent=UserAgent(**safe_get(self.ua, 'user_agent')),
            cpu=CPU(**safe_get(self.ua, 'cpu')),
            device=Device(**safe_get(self.ua, 'device')),
            engine=UserAgent(**safe_get(self.ua, 'engine')),
            os=OS(**safe_get(self.ua, 'os'))
        )
