import argparse
import tomllib
from typing import NotRequired, TypedDict, cast
import urllib.parse

from scrapy.crawler import Crawler, CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings

from sitefeed.spiders import ArticlesSpider


class FeedSettings(TypedDict):
    start_url: str
    allow: NotRequired[str | list[str]]
    restrict_css: NotRequired[str | list[str]]
    path: str


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
        feed_settings["path"]: {
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


parser = argparse.ArgumentParser(
    description="Gather articles from websites into Atom feeds"
)
parser.add_argument(
    "-c",
    "--config",
    type=argparse.FileType(mode='rb'),
    required=True,
    help="configuration file path",
)


if __name__ == "__main__":
    args = parser.parse_args()

    default_settings: Settings = get_project_settings()
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
            allow=feed_settings.get("allow"),
            restrict_css=feed_settings.get("restrict_css"),
        )

    process.start()
