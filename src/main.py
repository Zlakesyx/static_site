import node
from block.block_converter import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
)
from node.htmlnode import HTMLNode
from node.parentnode import ParentNode
from node.textnode import TextNode, TextType
from node.leafnode import LeafNode
from node.converter import text_node_to_html_node
from node.splitter import text_to_nodes


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)

    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            parent_node = ParentNode("p", text_to_children(block))
        elif block_type == BlockType.HEADING:
            count = block.count("#", 0, 6)
            block = block.lstrip("#" * count + " ")
            parent_node = ParentNode(f"h{count}", text_to_children(block))
        elif block_type == BlockType.CODE:
            block = block.strip("```")
            parent_node = code_parent(block)
        elif block_type == BlockType.QUOTE:
            block = block.replace(">", "")
            parent_node = ParentNode(
                "blockquote",
                [ParentNode("p", text_to_children(block))],
            )
        elif block_type == BlockType.UNORDERED_LIST:
            block = block.replace("- ", "")
            parent_node = ParentNode(
                "ul",
                [
                    ParentNode("li", [LeafNode(None, item)])
                    for item in block.split("\n")
                ],
            )
        elif block_type == BlockType.ORDERED_LIST:
            parent_node = ParentNode(
                "ol",
                [
                    ParentNode("li", [LeafNode(None, item.split(". ", 1)[1])])
                    for item in block.split("\n")
                ],
            )
        else:
            raise ValueError("Could not identify block type")
        children.append(parent_node)
    return ParentNode("div", children)


def text_to_children(block: str) -> list[HTMLNode]:
    # Remove line breaks for inline conversion
    text = block.replace("\n", " ")
    return [text_node_to_html_node(text_node) for text_node in text_to_nodes(text)]


def code_parent(block: str) -> ParentNode:
    return ParentNode(
        "pre",
        [ParentNode("code", [text_node_to_html_node(TextNode(block, TextType.TEXT))])],
    )


def main():
    print("testing")


if __name__ == "__main__":
    main()
