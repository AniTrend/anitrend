from typing import List
from dataclasses import dataclass


@dataclass
class NewsSchema:
    id: str
    title: str
    author: str
    description: str
    content: str
    image: str
    publishedOn: int
    link: str


@dataclass
class NewsConnectionSchema:
    count: int
    first: str
    last: str
    data: List[NewsSchema]
