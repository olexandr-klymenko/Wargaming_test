import feedparser
from rich import print_json

from src.parsers import EntryParser
from settings import RSS_FEED_URL


def main():
    feed = feedparser.parse(RSS_FEED_URL)
    for el in [el.json() for el in EntryParser(feed).parse()]:
        print_json(el)


if __name__ == "__main__":
    main()
