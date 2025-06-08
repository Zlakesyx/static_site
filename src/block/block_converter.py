from enum import Enum

import re


class BlockType(str, Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(text: str) -> list[str]:
    """
    # This is a heading

    This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

    - This is the first list item in a list block
    - This is a list item
    - This is another list item
    """
    blocks = text.strip().strip("\n").split("\n\n")
    return blocks


def block_to_block_type(block: str) -> BlockType:
    block = block.strip("\n").strip()
    if re.match(r"^(#{1,6})\s+(.*)", block):
        return BlockType.HEADING
    elif "".join(block[:3]) == "```" and "".join(block[-3:]) == "```":
        return BlockType.CODE
    elif _lines_match(block, ">"):
        return BlockType.QUOTE
    elif _lines_match(block, "- "):
        return BlockType.UNORDERED_LIST
    elif _is_ordered_list(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def _lines_match(block: str, delimeter: str) -> bool:
    lines = block.split("\n")
    for line in lines:
        match = re.match(rf"^{delimeter}.*", block)
        if not match:
            return False
    return True


def _is_ordered_list(block: str) -> bool:
    lines = block.split("\n")
    prev = 0
    for line in lines:
        current = re.findall(r"^(\d+)\.\s.*", line)
        if not current:
            return False
        if int(current[0]) - 1 != prev:
            return False
        prev += 1
    return True


def strip_block(block: str, block_type: BlockType) -> str:
    if block_type == BlockType.HEADING:
        count = block.count("#", 0, 6)
        return block.lstrip("#"*count + " ")
    elif block_type == BlockType.CODE:
        return block.strip("```")
    elif block_type == BlockType.QUOTE:
        return block.replace(">", "")
    #elif block_type == BlockType.UNORDERED_LIST:
    #elif block_type == BlockType.ORDERED_LIST:
    #else:
        return block

