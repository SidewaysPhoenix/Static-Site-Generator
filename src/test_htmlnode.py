import unittest

from htmlnode import HTMLNode, LeafNode


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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_url(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')