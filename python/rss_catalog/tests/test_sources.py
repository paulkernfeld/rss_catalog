from unittest import TestCase
import unittest

from rss_catalog.sources import strip_tree_leaves


class TestSources(TestCase):
    def test_strip_tree_leaves(self):
        self.assertEqual({}, strip_tree_leaves({1: {}}))

    def test_strip_tree_leaves_2(self):
        self.assertEqual({1: {}}, strip_tree_leaves({1: {2: {}}}))

if __name__ == "__main__":
    unittest.main()