from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class NewsSchema:
    id: str
    title: str
    link: str
    description: str
    content: str
    publishedOn: int
    author: Optional[str] = None
    category: Optional[str] = None
    genre: Optional[str] = None
    area: Optional[str] = None
    lang: Optional[str] = None
    image: Optional[str] = None


@dataclass
class NewsConnectionSchema:
    count: int
    first: Optional[str] = None
    last: Optional[str] = None
    data: List[NewsSchema] = field(default_factory=list)
