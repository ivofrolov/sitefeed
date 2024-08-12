import logging
from collections.abc import Iterable

import readability
from scrapy.http import Response
from scrapy.item import Field, Item

logging.getLogger("readability.readability").setLevel(logging.INFO)


class Article(Item):
    content = Field()
    title = Field()
    url = Field()


class ArticleExtractor:
    def __init__(
        self,
        *,
        min_text_length: int = 25,
        negative_keywords: Iterable[str] | None = None,
    ):
        self.min_text_length = min_text_length
        self.negative_keywords = negative_keywords

    def load_item(self, response: Response) -> Article:
        document = readability.Document(
            response.text,
            min_text_length=self.min_text_length,
            negative_keywords=self.negative_keywords,
        )
        return Article(
            content=document.summary(html_partial=True),
            title=document.short_title(),
            url=response.url,
        )
