from functions import split_nodes_delimiter
import unittest
from textnode import TextNode, TextType

class TestFunctions(unittest.TestCase):
    def test_delimeter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    
    def test_delimeter_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.BOLD)
    
    def test_delimeter_italic(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.ITALIC)
    
    
