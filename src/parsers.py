from abc import ABC, abstractmethod
import concurrent.futures
import re

from bs4 import BeautifulSoup
from loguru import logger
from pydantic import BaseModel, HttpUrl, ValidationError
import requests


class ImageParsingError(Exception):
    pass


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
    WGC_CLIENT_IMAGE_RE = re.compile(r"background-image: url\((.*)\)")

    def __init__(self, feed: "feedparser.util.FeedParserDict"):
        self._feed = feed

    def parse(self):
        logger.info("Parsing articles ...")
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

        logger.info("Start updating images ...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(self._update_image, [el for el in result if "wgc-client" in el.link])

        return result

    def _update_image(self, entry: ArticleInfo):
        logger.info(f"Updating image for article: '{entry.title}'")
        entry.image = self._get_image(entry.link)

    def _get_image(self, link):
        html = requests.get(link).text
        soup = BeautifulSoup(html, "html.parser")
        image_div = soup.find(class_="_backdrop")
        if new_image_re := self.WGC_CLIENT_IMAGE_RE.search(image_div.attrs["style"]):
            return new_image_re.group(1)

        raise ImageParsingError("Failed to parse image URL")
