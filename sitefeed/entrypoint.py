import argparse
import os
import tomllib
import urllib.parse
from pathlib import Path
from typing import NotRequired, TypedDict, cast

from scrapy.crawler import Crawler, CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

from sitefeed.spiders import (
    ArticleExtractorOptions,
    ArticlesSpider,
    LinkExtractorOptions,
)


class FeedSettings(TypedDict):
    start_url: str
    link_extractor: NotRequired[LinkExtractorOptions]
    article_extractor: NotRequired[ArticleExtractorOptions]


class LocalSettings(TypedDict, total=False):
    feed: dict[str, FeedSettings]


def update_feed_settings(
    crawler: Crawler,
    *,
    name: str,
    output_dir: Path,
    settings: FeedSettings,
) -> None:
    feeds = {
        output_dir.joinpath(name).with_suffix(".xml"): {
            "format": "atom",
            "encoding": "utf-8",
            "overwrite": True,
            "item_export_kwargs": {
                "title": name.title(),
                "link": settings["start_url"],
                "id_": urllib.parse.urljoin(settings["start_url"], "/"),
            },
        }
    }
    crawler.settings.set("FEEDS", feeds, priority="spider")


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
        "-o",
        "--output",
        type=Path,
        required=True,
        metavar="DIR",
        help="feeds output directory",
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

    loglevel = ("ERROR", "WARNING", "INFO", "DEBUG")[min(args.verbose, 3)]
    default_settings.set("LOG_LEVEL", loglevel, priority="cmdline")

    process = CrawlerProcess(settings=default_settings)

    local_settings = cast(LocalSettings, tomllib.load(args.config))
    for feed, feed_settings in local_settings.get("feed", dict()).items():
        crawler = process.create_crawler(ArticlesSpider)
        update_feed_settings(
            crawler,
            name=feed,
            output_dir=args.output,
            settings=feed_settings,
        )
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
