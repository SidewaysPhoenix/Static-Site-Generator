import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue

        split_node = node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise Exception("Invalid markdown: unmatched delimeter")

        for index in range(len(split_node)):
            part = split_node[index]
            if part == "":
                 continue
            if index % 2 == 0:
                new_text_node = TextNode(part, TextType.TEXT)
                new_list.append(new_text_node)
            else:
                new_delimeter_node = TextNode(part, text_type)
                new_list.append(new_delimeter_node)
    return new_list

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_images(old_nodes):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        extracted_images = extract_markdown_images(node.text)
        if extracted_images == []:
            new_list.append(node)
            continue
        working_text = node.text
        for image in extracted_images:
            image_alt = image[0]
            image_link = image[1]
            sections = working_text.split(f"![{image_alt}]({image_link})", 1)
            if sections[0] != "":
                new_list.append(TextNode(sections[0], TextType.TEXT))
            new_list.append(TextNode(image_alt, TextType.IMAGE, image_link))
            working_text = sections[1]
        if working_text:
            new_list.append(TextNode(working_text, TextType.TEXT))
    return new_list


def split_nodes_links(old_nodes):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        extracted_links = extract_markdown_links(node.text)
        if extracted_links == []:
            new_list.append(node)
            continue
        working_text = node.text
        for link in extracted_links:
            link_alt = link[0]
            link_url = link[1]
            sections = working_text.split(f"[{link_alt}]({link_url})", 1)
            if sections[0] != "":
                new_list.append(TextNode(sections[0], TextType.TEXT))
            new_list.append(TextNode(link_alt, TextType.LINK, link_url))
            working_text = sections[1]
        if working_text:
            new_list.append(TextNode(working_text, TextType.TEXT))
    return new_list