from abc import ABC, abstractmethod
import json

from bs4 import BeautifulSoup
from loguru import logger
from pydantic import HttpUrl, ValidationError
from pydantic import BaseModel


class ArticleInfo(BaseModel):
    title: str
    description: str
    link: HttpUrl
    image: HttpUrl


class BaseParser(ABC):
    @abstractmethod
    def parse(self) -> list[ArticleInfo]:
        ...


class EntryParser(BaseParser):
    def __init__(self, feed: "feedparser.util.FeedParserDict"):
        self._feed = feed

    def parse(self):
        result = []
        for entry in self._feed.get("entries", []):
            try:
                result.append(
                    ArticleInfo(
                        title=entry.title,
                        description=BeautifulSoup(entry.summary, "html.parser")
                        .find_all("div")[0]
                        .text.strip(),
                        link=entry.link,
                        image=entry.links[1]["href"],
                    )
                )
            except ValidationError as err:
                logger.error(err)

        return result
