from scrapy.linkextractors import LinkExtractor
from scrapy.http import Response
from scrapy.spiders import CrawlSpider, Rule
from w3lib.url import parse_url

from sitefeed.items import Article, ArticleLoader


class ArticlesSpider(CrawlSpider):
    name = "articles"

    def __init__(
        self,
        *args,
        start_url: str,
        allow: str | list[str] | None = None,
        restrict_css: str | list[str] | None = None,
        **kwargs,
    ):
        self.start_urls = [start_url]
        self.rules = [
            Rule(
                LinkExtractor(
                    allow=allow,
                    restrict_css=restrict_css,
                    allow_domains=parse_url(start_url).hostname,
                ),
                callback=self.parse_article,
            )
        ]
        super().__init__(*args, **kwargs)

    def parse_article(self, response: Response) -> Article:
        return ArticleLoader(response).load_item()
