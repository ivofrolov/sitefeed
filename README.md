# SiteFeed

Extracts RSS[^1] feed from websites that doesn't support that.

Fully manual operation.

## Usage

Create configuration file in TOML format with fhe followin structure.

``` toml
[feed.example]                         # <example> is a feed name
start_url = "https://www.example.com/" # web page containing links to articles
link_extractor = {
    allow = "/articles/",              # regexp that the article links must match (not required)
    restrict_css = ".links"            # css selector of region where links should be extracted from (not required)
}
article_extractor = {
    restrict_css = "article"           # css selector of region where article should be extracted from (not required)
}
output = "example.xml"                 # path to store Atom feed

[feed.another]
# etc.
```

Then start crawling process.

`python -m sitefeed -c config.toml`

[^1]: Atom actually
