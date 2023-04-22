import logging

import readability
from scrapy.item import Item, Field
from scrapy.http import Response


logging.getLogger("readability.readability").setLevel(logging.INFO)


class Article(Item):
    content = Field()
    title = Field()
    url = Field()


class ArticleLoader:
    def __init__(self, response: Response):
        self.response = response

    def load_item(self) -> Article:
        document = readability.Document(self.response.text)
        return Article(
            content=document.summary(html_partial=True),
            title=document.short_title(),
            url=self.response.url,
        )
