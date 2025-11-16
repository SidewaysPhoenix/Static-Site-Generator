from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    BOLD = "bold"
    TEXT = "text"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"



class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (
            self.text == other.text and 
            self.text_type == other.text_type and
            self.url == other.url
        ):
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    tt = text_node.text_type
    txt = text_node.text

    if tt == TextType.TEXT:
        return LeafNode(None, txt)
    elif tt == TextType.BOLD:
        return LeafNode("b", txt)
    elif tt == TextType.ITALIC:
        return LeafNode("i", txt)
    elif tt == TextType.CODE:
        return LeafNode("code", txt)
    elif tt == TextType.LINK:
        return LeafNode("a", txt, {"href": text_node.url})
    elif tt == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": txt})
    else:
        raise Exception("Unknown TextType")