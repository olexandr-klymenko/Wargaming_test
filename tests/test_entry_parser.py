import json
from unittest import TestCase

import feedparser

from src.parsers import EntryParser

FEED_SOURCE = """
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="/en/rss/news/rss.xsl" media="screen"?>
<rss version="2.0"
     xmlns:content="http://purl.org/rss/1.0/modules/content/"
     xmlns:wfw="http://wellformedweb.org/CommentAPI/"
     xmlns:dc="http://purl.org/dc/elements/1.1/"
     xmlns:atom="http://www.w3.org/2005/Atom"
     xmlns:sy="http://purl.org/rss/1.0/modules/syndication/"
     xmlns:slash="http://purl.org/rss/1.0/modules/slash/"
>
    <channel>
        <title>News</title>
        <atom:link href="https://worldofwarships.com/en/rss/news/" rel="self" type="application/rss+xml" />
        <link>https://worldofwarships.com/en/news/</link>
        <description>News archive</description>
        <language> en </language>
        <pubDate>Wed, 03 Nov 2021 17:31:02 GMT</pubDate>
        <ttl>300</ttl>

        <image>
            <url>//wows-static-production.gcdn.co/wowsp/ee7beef1/portalnews/images/wows_rss.png</url>
            <title>News</title>
            <link>https://worldofwarships.com/en/news/</link>
        </image>

            <item>
                <title>Naval Legends: USS Torsk</title>
                <link>https://worldofwarships.com/en/news/general-news/naval-legends-torsk/</link>
                <description>
                    <![CDATA[<div>
    In this episode, we’ll learn about the famous WWII submarine that’s now preserved at Baltimore Harbor.
</div>

<div>
    <a href="https://worldofwarships.com/en/news/general-news/naval-legends-torsk/">Read more</a>
</div>]]>
                </description>
                <guid isPermaLink="true">https://worldofwarships.com/en/news/general-news/naval-legends-torsk/</guid>
                <pubDate>Wed, 03 Nov 2021 13:00:00 GMT</pubDate>
                <category domain="https://worldofwarships.com/en/news/general-news/">General News</category>
                <enclosure url="https://wowsp-wows-na.wgcdn.co/dcont/fb/image/tmb/b028b6d2-37d2-11ec-9e7a-8cdcd4b147d4_1200x.jpg" length="115927" type="image/jpeg" />
            </item>
    </channel>
</rss>
"""


class TestEntryParser(TestCase):
    def test_entry_parser(self):
        result = [json.loads(el.json()) for el in EntryParser(feedparser.parse(FEED_SOURCE)).parse()]
        expected = [
            {
                "title": "Naval Legends: USS Torsk",
                "description": "In this episode, we’ll learn about the famous WWII"
                " submarine that’s now preserved at Baltimore Harbor.",
                "link": "https://worldofwarships.com/en/news/general-news/naval-legends-torsk/",
                "image": "https://wowsp-wows-na.wgcdn.co"
                "/dcont/fb/image/tmb/b028b6d2-37d2-11ec-9e7a-8cdcd4b147d4_1200x.jpg",
            }
        ]
        self.assertEqual(result, expected)

    def test_entry_parser_fail(self):
        source = "<link>https://worldofwarships.com/en/news/general-news/naval-legends-torsk/</link>"
        invalid = "<link>httpworldofwarships.com/en/news/general-news/naval-legends-torsk/</link>"
        result = EntryParser(
            feedparser.parse(FEED_SOURCE.replace(source, invalid))
        ).parse()
        self.assertEqual(result, [])
