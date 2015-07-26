#!/usr/bin/env python
"""
Add RSS links from an HTML file that contains links to RSS feeds.
"""
import argparse
from collections import defaultdict
from urlparse import urljoin
from bs4 import BeautifulSoup
from sys import argv

import requests
from rss_catalog.sources import add_source_interactive, url_to_name, SOURCE_NAME_REGEX


def add_links_from_html(url, modify_link_url=None, modify_source_name=None):
    page = requests.get(url)
    soup = BeautifulSoup(page.text)

    hrefs = defaultdict(set)
    for link in soup.find_all('a'):
        href = link.get("href")

        if href is None:
            # Remove junk links
            continue

        # Resolve relative URLs
        href = urljoin(url, href)

        if not href.startswith("http"):
            # Remove junk links
            continue

        if href == url:
            # Don't include the same page!
            continue

        if modify_link_url:
            href = modify_link_url(href)

        if "rd.yahoo." in href or "my.yahoo." in href:
            # Yahoo Reader add button
            continue

        if "rss" in href or ".xml" in href:
            hrefs[href].add(href)

            hrefs[href].add(link.get("title"))

            # could also go up the tree trying to get the text
            hrefs[href].add(link.string)

            # Filter out Nones
            hrefs[href] = set(h for h in hrefs[href] if h is not None)

    for href, info in sorted(hrefs.iteritems()):
        source_name = url_to_name(href)
        source_name = modify_source_name(source_name)
        if SOURCE_NAME_REGEX.match(source_name) is None:
            continue
        add_source_interactive(source_name, href, " ".join(info))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add RSS links from an HTML page.')
    parser.add_argument('url', type=str, help='the URL of the HTML page')
    parser.add_argument('modify_link_url', type=str)
    parser.add_argument('modify_source_name', type=str)

    args = parser.parse_args(argv[1:])

    modify_link_url = None
    if args.modify_link_url:
        modify_link_url = lambda link_url : eval(args.modify_link_url, {}, {"link_url": link_url})

    modify_source_name = None
    if args.modify_source_name:
        modify_source_name = lambda source_name : eval(args.modify_source_name, {}, {"source_name": source_name})

    add_links_from_html(args.url, modify_link_url, modify_source_name)