from textnode import TextNode, TextType


def main():
    printing = TextNode("text", TextType.LINK, "www.link.com")
    print(printing)

main()