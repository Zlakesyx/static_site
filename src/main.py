import copy
import re

from node.textnode import TextNode, TextType
from node.leafnode import LeafNode


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    #![rick roll](https://i.imgur.com/aKaOqIh.gif)
    pattern = r"\!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    # [youtube](https://www.youtube.com)
    pattern = r"\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)


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


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"{text_node.text_type} is not a value TextType")


def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)
    print(
        extract_markdown_images(
            "This is an image: ![rick roll](https://i.imgur.com/aKaOqIh.gif). end."
        )
    )
    print(
        extract_markdown_links(
            "This is an link: [youtube](https://www.youtube.com). end."
        )
    )


if __name__ == "__main__":
    main()
