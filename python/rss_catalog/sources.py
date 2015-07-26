#!/usr/bin/env python
import json
import os
import re

import feedparser
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.shortcuts import get_input
from prompt_toolkit.validation import Validator, ValidationError


ROOT = "../resources"
SOURCE_LIST_PATH = os.path.join(ROOT, "source_list.json")
SOURCE_TREE_PATH = os.path.join(ROOT, "source_tree.json")

# A URL without the protocol, but not ending in a slash
SOURCE_NAME_REGEX = re.compile('^([^\.\/]+\.)+[^\.\/]+(\/[^\/]+)*$')


def official_json_dump(content, file_object):
    json.dump(content, file_object, sort_keys=True, indent=2, separators=(',', ': '))


def get_source_list():
    with open(SOURCE_LIST_PATH) as source_list_file:
        return json.load(source_list_file)


def write_source_list(source_list, path=SOURCE_LIST_PATH):
    with open(path, 'w') as source_list_file:
        official_json_dump(source_list, source_list_file)


def get_source_tree():
    with open(SOURCE_TREE_PATH) as source_tree_file:
        return json.load(source_tree_file)


def write_source_tree(source_tree, path=SOURCE_TREE_PATH):
    with open(path, 'w') as source_tree_file:
        official_json_dump(source_tree, source_tree_file)


def normalize():
    write_source_list(get_source_list())
    write_source_tree(get_source_tree())


def url_to_name(url):
    name = url[url.find("://") + 3:]
    if "#" in name:
        name = name[:name.find("#")]
    if "?" in name:
        name = name[:name.find("?")]
    if name.endswith("index.html"):
        name = name[:-len("index.html")]
    return name.rstrip("/")


def make_source_list_entry(rss_url, proportion):
    return {
        'rss_url': rss_url,
        'article_proportion': proportion
    }


def strip_tree_leaves(tree):
    return {
        k: strip_tree_leaves(v)
        for k, v in tree.viewitems()
        if v != {}
    }


def tree_to_paths(tree, prefix=[]):
    if tree == {}:
        return [prefix]
    else:
        x = []
        for key, value in tree.viewitems():
            x += tree_to_paths(value, prefix + [key])
        return x


class SetValidator(Validator):
    def __init__(self, inputs):
        self.inputs = inputs

    def validate(self, document):
        if document.text not in self.inputs:
            raise ValidationError(message='Please enter one of: {}'.format(", ".join(self.inputs)), index=len(document.text))


class YnValidator(SetValidator):
    def __init__(self):
        super(YnValidator, self).__init__({"y", "n"})


class ProportionValidator(Validator):
    def validate(self, document):
        error = ValidationError(message='Please enter a proportion 0.0 < p <= 1.0.', index=len(document.text))
        try:
            if not 0.0 < float(document.text) <= 1.0:
                raise error
        except ValueError:
            raise error


class WordListValidator(Validator):
    def __init__(self, word_list):
        self.word_list = word_list

    def validate(self, document):
        if document.text not in self.word_list:
            raise ValidationError(message='Please a word from the list.', index=len(document.text))


def add_to_tree_interactive(source_tree, path_to_new_source, source_name):
    """
    MODIFIES IN PLACE.

    :param source_tree:
    :param list[str] path_to_new_source:
    :param source_name:
    :return: True if this was added, otherwise false
    """
    node = source_tree
    for child in path_to_new_source:
        if child not in node:
            if 'y' == get_input(u'Add child {}? '.format(child), validator=YnValidator()):
                node[child] = {}
            else:
                return False
        node = node[child]
    node[source_name] = {}
    return True


def add_source_interactive(source_name, source_rss, source_info=None):
    if SOURCE_NAME_REGEX.match(source_name) is None:
        raise ValueError("Source name {} didn't match regex".format(source_name))

    parsed = feedparser.parse(source_rss)
    if "bozo_exception" in parsed:
        print "Couldn't parse: {} {}".format(source_rss, parsed["bozo_exception"])
        return False

    link = url_to_name(parsed.feed.link)
    # TODO check that link is a real page
    if link != source_name:
        print "Warning: source name != name from feed link: {} != {}".format(source_name, link)

    print "Source name: {}".format(source_name)
    print "Source RSS url: {}".format(source_rss)
    print "Source info: {}".format(source_info)
    if 'n' == get_input(u'Add this source? ', validator=YnValidator()):
        return

    source_list = get_source_list()
    if source_name in source_list:
        if 'n' == get_input(
                u'Replace existing source? {} '.format(source_list[source_name]),
                validator=YnValidator()
        ):
            return

    proportion = float(get_input(u'Proportion of entries that are articles: ', validator=ProportionValidator()))

    source_list[source_name] = make_source_list_entry(source_rss, proportion)
    write_source_list(source_list)
    print "Source added\n"

    source_tree = get_source_tree()
    paths = [":".join(path) for path in tree_to_paths(strip_tree_leaves(source_tree))]
    path = get_input(
        u'Where? ',
        completer=WordCompleter(paths, match_middle=True)
    )
    if add_to_tree_interactive(source_tree, path.split(":"), source_name):
        write_source_tree(source_tree)
        print "Source added to tree at {}\n".format(path)
    else:
        print "Source not added"


if __name__ == "__main__":
    normalize()
