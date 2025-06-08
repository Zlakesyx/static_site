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
    blocks = text.strip().split("\n\n")
    return blocks


def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^(#{1,6})\s+(.*)", block):
        return BlockType.HEADING
    elif re.match(r"^(`{3})(.*)(`{3})$", block):
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
