from datetime import datetime, timezone
from xml.sax.saxutils import XMLGenerator

from scrapy.exporters import BaseItemExporter

from sitefeed.spiders import Article


class AtomArticleExporter(BaseItemExporter):
    def __init__(
        self,
        file,
        *,
        title: str = "Example Feed",
        link: str = "http://example.com/",
        id_: str = "http://example.com/",
        **kwargs,
    ):
        super().__init__(**kwargs)

        if not self.encoding:
            self.encoding = "utf-8"
        self.xg = XMLGenerator(file, encoding=self.encoding)

        self.title = title
        self.link = link
        self.id_ = id_

    def _newline_and_indent(self, depth: int = 1) -> None:
        self.xg.characters("\n")
        if self.indent:
            self.xg.characters(" " * self.indent * depth)

    def start_exporting(self) -> None:
        self.xg.startDocument()

        self.xg.startElement("feed", {"xmlns": "http://www.w3.org/2005/Atom"})

        self._newline_and_indent(depth=1)
        self.xg.startElement("title", {})
        self.xg.characters(self.title)
        self.xg.endElement("title")

        self._newline_and_indent(depth=1)
        self.xg.startElement("link", {"href": self.link})
        self.xg.endElement("link")

        self._newline_and_indent(depth=1)
        self.xg.startElement("updated", {})
        self.xg.characters(datetime.now(timezone.utc).isoformat(timespec='seconds'))
        self.xg.endElement("updated")

        self._newline_and_indent(depth=1)
        self.xg.startElement("id", {})
        self.xg.characters(self.id_)
        self.xg.endElement("id")

    def export_item(self, item: Article):
        self._newline_and_indent(depth=1)
        self.xg.startElement("entry", {})

        self._newline_and_indent(depth=2)
        self.xg.startElement("title", {})
        self.xg.characters(item["title"])
        self.xg.endElement("title")

        self._newline_and_indent(depth=2)
        self.xg.startElement("content", {"type": "html"})
        self.xg.characters(item["content"])
        self.xg.endElement("content")

        self._newline_and_indent(depth=2)
        self.xg.startElement("link", {"href": item["url"]})
        self.xg.endElement("link")

        self._newline_and_indent(depth=2)
        self.xg.startElement("id", {})
        self.xg.characters(item["url"])
        self.xg.endElement("id")

        self._newline_and_indent(depth=1)
        self.xg.endElement("entry")

    def finish_exporting(self):
        self._newline_and_indent(depth=1)
        self.xg.endElement("feed")
        self.xg.endDocument()
