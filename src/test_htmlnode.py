import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_href(self):
        node1 = HTMLNode("tag", "value", None, {"href": "https://google.com", "target": "_blank",})
        node1.props_to_html()

    def test_print_node(self):
        node1 = HTMLNode("tag", "value", None, {"href": "https://google.com", "target": "_blank",})
        print(node1)

    def test_lots_of_things(self):
        node1 = HTMLNode("tag", "value", None, {
            "href": "https://google.com", 
            "target": "_blank",
            "other": "some_thing",
            "stuff": "other_stuff",
            })
        node1.props_to_html()