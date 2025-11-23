import re
import os
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode, ParentNode
from block_types import block_to_block_type, BlockType

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

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

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = []
    for block in blocks:
        if block == "":
            continue
        stripped_blocks.append(block.strip()) 
    return stripped_blocks

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    block_children = []
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        
        #if paragraph
        if block_type == BlockType.PARAGRAPH:
            lines = block.split("\n")
            paragraph_text = " ".join(lines)
            children = text_to_children(paragraph_text)

            node = ParentNode("p", children)
            block_children.append(node)
        
        #if Unordered List
        elif block_type == BlockType.UNORDERED_LIST:
            split_list_from_block = block.split("\n")
            list_item_nodes = []
            for line in split_list_from_block:
                new_line = line.strip("- ")
                children = text_to_children(new_line)
                li_parent_node = ParentNode("li", children)
                list_item_nodes.append(li_parent_node)
            node = ParentNode("ul", list_item_nodes)
            block_children.append(node)

        #if Ordered List
        elif block_type == BlockType.ORDERED_LIST:
            split_list_from_block = block.split("\n")
            list_item_nodes = []
            for line in split_list_from_block:
                dot_index = line.find(". ")
                if dot_index == -1:
                    new_line = line
                else:
                    new_line = line[dot_index + 2 :]
                children = text_to_children(new_line)
                li_parent_node = ParentNode("li", children)
                list_item_nodes.append(li_parent_node)
            
            
            node = ParentNode("ol", list_item_nodes)
            block_children.append(node)

        #if Code
        elif block_type == BlockType.CODE:
            lines = block.split("\n")
            inner_lines = lines[1:-1]
            code_text = "\n".join(inner_lines)

            text_node = TextNode(code_text, TextType.TEXT)
            code_child = text_node_to_html_node(text_node)

            code_parent_node = ParentNode("code", [code_child])
            node = ParentNode("pre", [code_parent_node])
            block_children.append(node)

        #if Heading
        elif block_type == BlockType.HEADING:
            pound_count = 0
            for c in block:
                if c == '#':
                    pound_count += 1
                else:
                    break
            heading_text = block[pound_count + 1 :]
            children = text_to_children(heading_text)
            node = ParentNode(f"h{pound_count}", children)
            block_children.append(node)

        
        #if Quote
        elif block_type == BlockType.QUOTE:
            split_list_from_block = block.split("\n")
            new_lines = []
            for line in split_list_from_block:
                cleaned = line.lstrip(">").strip()
                new_lines.append(cleaned)
                
            content = " ".join(new_lines)
            children = text_to_children(content)
            node = ParentNode("blockquote", children)
            block_children.append(node)

    return ParentNode("div", block_children)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for tn in text_nodes:
        child = text_node_to_html_node(tn)
        children.append(child)
    return children

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block.strip("#").strip()
    raise Exception("No header in markdown")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    with open(from_path, "r") as f:
        markdown_contents = f.read()
    with open(template_path, "r") as f:
        template_contents = f.read()

    html_node = markdown_to_html_node(markdown_contents)
    html_string = html_node.to_html()

    title = extract_title(markdown_contents)

    updated_template_title = template_contents.replace("{{ Title }}", title)
    full_html_page = updated_template_title.replace("{{ Content }}", html_string)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":    
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(full_html_page)

