#!/usr/bin/env python
from copy import copy
from sys import argv

# Source name is the arg
from rss_catalog.sources import get_source_list, write_source_list, get_source_tree, write_source_tree

source_name = argv[1]

source_list = get_source_list()
try:
    del source_list[source_name]
except KeyError:
    print "Not in source list"
write_source_list(source_list)


def del_from_tree(tree):
    for key, value in copy(tree).viewitems():
        if key == source_name:
            del tree[source_name]
        elif value != {}:
            del_from_tree(value)


source_tree = get_source_tree()
del_from_tree(source_tree)
write_source_tree(source_tree)