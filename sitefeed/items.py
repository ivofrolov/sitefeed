import logging

import readability
from scrapy.item import Item, Field
from scrapy.http import Response


logging.getLogger("readability.readability").setLevel(logging.INFO)


class Article(Item):
    content = Field()
    title = Field()
    url = Field()


class ArticleExtractor:
    restrict_css: str

    def __init__(self, *, restrict_css: str | None = None):
        self.restrict_css = restrict_css or "html"

    def load_item(self, response: Response) -> Article:
        document = readability.Document(response.css(self.restrict_css).get())
        return Article(
            content=document.summary(html_partial=True),
            title=document.short_title(),
            url=response.url,
        )
