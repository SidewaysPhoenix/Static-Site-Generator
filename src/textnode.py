from enum import Enum


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
            self.TextNode.text == other.TextNode.text and 
            self.TextNode.text_type == other.TextNode.text_type and
            self.TextNode.url == other.TextNode.url
        ):
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
