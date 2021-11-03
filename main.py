from argparse import ArgumentParser

import feedparser
from rich import print_json

from src.parsers import EntryParser
from settings import RSS_FEED_URL


def main(url=RSS_FEED_URL):
    feed = feedparser.parse(url)
    for el in [el.json() for el in EntryParser(feed).parse()]:
        print_json(el)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-u", "--url", default=RSS_FEED_URL, help="RSS feed URL")
    args = parser.parse_args()
    main(args.url)
