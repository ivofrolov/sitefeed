from typing import TypedDict

from scrapy.linkextractors import LinkExtractor
from scrapy.http import Response
from scrapy.spiders import CrawlSpider, Rule
from w3lib.url import parse_url

from sitefeed.items import Article, ArticleExtractor
from sitefeed.utils import extract_options


class LinkExtractorOptions(TypedDict, total=False):
    allow: str | list[str]
    restrict_css: str | list[str]


class ArticleExtractorOptions(TypedDict, total=False):
    restrict_css: str | None


class ArticlesSpider(CrawlSpider):
    name = "articles"

    def __init__(
        self,
        *args,
        start_url: str,
        **kwargs,
    ):
        self.start_urls = [start_url]
        self.allowed_domains = [parse_url(start_url).hostname]

        link_extractor_options = extract_options(
            r"link_extractor_", kwargs, LinkExtractorOptions
        )
        self.rules = [
            Rule(
                LinkExtractor(**link_extractor_options),
                callback=self.parse,
            )
        ]

        article_extractor_options = extract_options(
            r"article_extractor_", kwargs, ArticleExtractorOptions
        )
        self.article_extractor = ArticleExtractor(**article_extractor_options)

        super().__init__(*args, **kwargs)

    def parse(self, response: Response) -> Article:
        return self.article_extractor.load_item(response)
