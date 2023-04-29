import argparse
import os
import tomllib
from typing import NotRequired, TypedDict, cast
import urllib.parse

from scrapy.crawler import Crawler, CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings

from sitefeed.spiders import (
    ArticlesSpider,
    ArticleExtractorOptions,
    LinkExtractorOptions,
)


class FeedSettings(TypedDict):
    start_url: str
    output: str
    link_extractor: NotRequired[LinkExtractorOptions]
    article_extractor: NotRequired[ArticleExtractorOptions]


class LocalSettings(TypedDict, total=False):
    feed: dict[str, FeedSettings]


def derive_feed_settings(
    *,
    feed: str,
    feed_settings: FeedSettings,
    default_settings: Settings,
) -> Settings:
    settings = default_settings.copy()
    feeds = {
        feed_settings["output"]: {
            "format": "atom",
            "encoding": "utf8",
            "overwrite": True,
            "item_export_kwargs": {
                "title": feed.title(),
                "link": feed_settings["start_url"],
                "id_": urllib.parse.urljoin(feed_settings["start_url"], "/"),
            },
        }
    }
    settings.set("FEEDS", feeds, priority="spider")
    return settings


def crawl():
    parser = argparse.ArgumentParser(
        description="Gather articles from websites into Atom feeds"
    )
    parser.add_argument(
        "-c",
        "--config",
        type=argparse.FileType(mode="rb"),
        required=True,
        metavar="CONFIG.TOML",
        help="configuration file path",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="increase verbosity (add more to increase further)",
    )
    args = parser.parse_args()

    os.environ["SCRAPY_SETTINGS_MODULE"] = "sitefeed.settings"
    default_settings: Settings = get_project_settings()

    loglevel = ("ERROR", "INFO", "DEBUG")[min(args.verbose, 2) % 3]
    default_settings.set("LOG_LEVEL", loglevel, priority="cmdline")

    process = CrawlerProcess(settings=default_settings)

    local_settings = cast(LocalSettings, tomllib.load(args.config))
    init_reactor = True
    for feed, feed_settings in local_settings.get("feed", dict()).items():
        crawler = Crawler(
            ArticlesSpider,
            settings=derive_feed_settings(
                feed=feed,
                feed_settings=feed_settings,
                default_settings=default_settings,
            ),
            init_reactor=init_reactor,
        )
        init_reactor = False
        process.crawl(
            crawler,
            start_url=feed_settings["start_url"],
            **{
                f"link_extractor_{key}": value
                for key, value in feed_settings.get("link_extractor", {}).items()
            },
            **{
                f"article_extractor_{key}": value
                for key, value in feed_settings.get("article_extractor", {}).items()
            },
        )

    process.start()
