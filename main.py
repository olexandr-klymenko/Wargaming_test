import feedparser

from src.parsers import EntryParser
from settings import RSS_FEED_URL


def main():
    feed = feedparser.parse(RSS_FEED_URL)
    print(EntryParser(feed).parse())


if __name__ == "__main__":
    main()
