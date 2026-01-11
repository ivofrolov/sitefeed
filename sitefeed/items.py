import re

from itemloaders.processors import MapCompose, TakeFirst
from lxml_html_clean import Cleaner
from scrapy.http import TextResponse
from scrapy.item import Field, Item
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags


class Article(Item):
    content = Field()
    title = Field()
    url = Field()


class ArticleLoader(ItemLoader):
    default_item_class = Article
    default_output_processor = TakeFirst()


class ArticleExtractor:
    cleaner = Cleaner(
        style=True,
        # other options left default
    )

    @staticmethod
    def clean_whitespace(value: str) -> str:
        if not value:
            return value
        return re.sub(r"\s+", " ", value).strip()

    def __init__(self, *, title_css: str = "title", content_css: str = "article"):
        self.title_css = title_css
        self.content_css = content_css

    def load_item(self, response: TextResponse) -> Article:
        loader = ArticleLoader(response=response)
        loader.add_css(
            "title",
            self.title_css,
            MapCompose(remove_tags, self.clean_whitespace),
        )
        loader.add_css("content", self.content_css, MapCompose(self.cleaner.clean_html))
        loader.add_value("url", response.url)
        return loader.load_item()
