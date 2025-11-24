import re
from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = []
    for block in blocks:
        if block == "":
            continue
        stripped_blocks.append(block.strip()) 
    return stripped_blocks

def block_to_block_type(markdown_block):
    split_lines = markdown_block.split("\n")
    #headings section
    if re.match(r"^#{1,6} .+", split_lines[0]):
        return BlockType.HEADING

    #code section
    elif markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE 
        
    #quote section
    elif markdown_block.startswith(">"):
        for line in split_lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    #unordered_list section
    elif markdown_block.startswith("- "):
        for line in split_lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    #ordered_list
    elif markdown_block.startswith("1. "):
        expected = 1
        for line in split_lines:
            line = line.strip()
            if not line.startswith(f"{expected}. "):
                return BlockType.PARAGRAPH
            expected += 1
        return BlockType.ORDERED_LIST   

    else: 
        return BlockType.PARAGRAPH

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