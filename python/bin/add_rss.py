#!/usr/bin/env python
from datetime import datetime
from sys import argv
from time import mktime

import feedparser

from rss_catalog.sources import add_source_interactive, url_to_name


# Usage: add_rss.py rss_url [source_name]

feed_url = argv[1]
d = feedparser.parse(feed_url)
try:
    updated = str(datetime.fromtimestamp(mktime(d['updated_parsed'])))
except KeyError:
    updated = "???"
name = url_to_name(d['feed']['link'])

info = "Updated {}".format(updated)

if len(argv) > 2:
    name = argv[2]

add_source_interactive(name, feed_url, source_info=info)
