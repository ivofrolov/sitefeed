from typing import Any, TypedDict

from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from w3lib.url import parse_url

from sitefeed.items import Article, ArticleExtractor


class LinkExtractorOptions(TypedDict, total=False):
    allow: str | list[str]
    restrict_css: str | list[str]


class ArticleExtractorOptions(TypedDict, total=False):
    min_text_length: int
    negative_keywords: list[str]


class ArticlesSpider(CrawlSpider):
    name = "articles"

    @staticmethod
    def _extract_options(prefix: str, options: dict[str, Any]) -> dict[str, Any]:
        return {
            key.removeprefix(prefix): value
            for key, value in options.items()
            if key.startswith(prefix)
        }

    def __init__(
        self,
        *args,
        start_url: str,
        **kwargs,
    ):
        self.start_urls = [start_url]
        self.allowed_domains = [parse_url(start_url).hostname]

        link_extractor_options = LinkExtractorOptions(
            **self._extract_options("link_extractor_", kwargs)
        )
        self.rules = [
            Rule(
                LinkExtractor(**link_extractor_options),
                callback=self.parse,
            )
        ]

        article_extractor_options = ArticleExtractorOptions(
            **self._extract_options("article_extractor_", kwargs)
        )
        self.article_extractor = ArticleExtractor(**article_extractor_options)

        super().__init__(*args, **kwargs)

    def parse(self, response: Response) -> Article:
        return self.article_extractor.load_item(response)
