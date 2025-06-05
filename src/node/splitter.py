import copy

from node import extractor
from node.textnode import TextNode, TextType


def text_to_nodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    return nodes


def split_nodes_images(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(copy.deepcopy(node))
            continue

        links = extractor.extract_markdown_images(node.text)
        if not links:
            new_nodes.append(copy.deepcopy(node))
            continue

        after = []
        temp_text = node.text
        for description, url in links:
            delimiter = f"![{description}]({url})"
            # This gets before and after
            before, after = temp_text.split(delimiter, maxsplit=1)
            new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(description, TextType.IMAGE, url))
            temp_text = after

        if after:
            new_nodes.append(TextNode(after, TextType.TEXT))

    return new_nodes


def split_nodes_links(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(copy.deepcopy(node))
            continue

        links = extractor.extract_markdown_links(node.text)
        if not links:
            new_nodes.append(copy.deepcopy(node))
            continue

        after = []
        temp_text = node.text
        for description, url in links:
            delimiter = f"[{description}]({url})"
            # This gets before and after
            before, after = temp_text.split(delimiter, maxsplit=1)
            new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(description, TextType.LINK, url))
            temp_text = after

        if after:
            new_nodes.append(TextNode(after, TextType.TEXT))

    return new_nodes


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType,
) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(copy.deepcopy(node))
            continue

        buffer = node.text.split(delimiter)
        if len(buffer) % 2 == 0:
            raise ValueError(
                f"Invalid Markdown syntax. Unclosed delimiter [{delimiter}]"
            )

        # Matches will be every odd index, not including 1st and last
        for i, text in enumerate(buffer):
            if not text:
                continue
            elif i % 2 == 1 and not (i == 0 or i == len(buffer) - 1):
                new_nodes.append(TextNode(text, text_type))
            else:
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes
