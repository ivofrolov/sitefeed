# SiteFeed

Extracts RSS feed from websites that don't support that.

Fully manual operation.

## Usage

Create configuration file in TOML format with fhe followin structure.

``` toml
[feed.example]                         # <example> is a feed name
start_url = "https://www.example.com/" # web page containing links to articles
allow = "/shop/"                       # regexp that the article links must match (not required)
restrict_css = ".products"             # css selector of regions where links should be extracted from (not required)
path = "example.xml"                   # path to store Atom feed

[feed.another]
# etc.
```

Then start crawling process.

`python -m sitefeed -c config.toml`
