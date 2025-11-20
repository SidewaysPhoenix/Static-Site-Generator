from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

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