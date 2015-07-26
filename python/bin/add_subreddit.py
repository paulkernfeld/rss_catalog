#!/usr/bin/env python
from sys import argv

from rss_catalog.reddit import add_subreddit


subreddit_url = argv[1]
add_subreddit(subreddit_url, "")