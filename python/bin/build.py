#!/usr/bin/env python
from rss_catalog.sources import get_source_tree, write_source_tree, get_source_list, write_source_list

source_list = get_source_list()
write_source_list(source_list, path="../build/source_list.json")

source_tree = get_source_tree()
write_source_tree(source_tree, path="../build/source_tree.json")