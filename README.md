# SiteFeed

Extracts RSS[^1] feed from websites that don't support it.

## Installation

``` shell
pip install sitefeed@git+https://github.com/ivofrolov/sitefeed.git
```

## Usage

Create a TOML configuration file of fhe following structure.

``` toml
[feed.example]                         # <example> is a feed name
start_url = "https://www.example.com/" # web page containing links to articles
link_extractor = {
    allow = "/articles/",              # regexp that article links must match (not required)
    restrict_css = ".links",           # css selector of a region links should be extracted from (not required)
}
article_extractor = {
    min_text_length = 25,              # higher value leads to more precise detection of longer texts (not required)
    negative_keywords = ["footer"],    # patterns in classes and ids that decrease content candidates score (not required)
}
output = "example.xml"                 # path to store feed

[feed.another]
# ...
```

And start a crawling process.

``` shell
sitefeed -c config.toml -o feeds
```

## GitHub Action

You can also fork this repository and get your own feeds hosted by
GitHub pages. The repo contains scheduled action that updates feeds
every day.

[^1]: Atom actually
