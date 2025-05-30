import unittest

from node.leafnode import LeafNode
from node.textnode import TextNode, TextType
from main import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    text_node_to_html_node,
)

props = {
    "href": "https://www.google.com",
    "target": "_blank",
}


class TestMain(unittest.TestCase):

    def test_text(self):
        node = TextNode("text node", TextType.TEXT)
        html_node: LeafNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "text node")

    def test_bold(self):
        node = TextNode("bold node", TextType.BOLD)
        html_node: LeafNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold node")

    def test_italic(self):
        node = TextNode("italic node", TextType.ITALIC)
        html_node: LeafNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic node")

    def test_code(self):
        node = TextNode("code node", TextType.CODE)
        html_node: LeafNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "code node")

    def test_link(self):
        node = TextNode("link node", TextType.LINK, "url.com")
        html_node: LeafNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "link node")
        self.assertEqual(html_node.props, {"href": "url.com"})

    def test_image(self):
        node = TextNode("image node", TextType.IMAGE, "url.com")
        html_node: LeafNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "url.com", "alt": "image node"})

    def test_split_nodes_delimiter_all_text(self):
        nodes = [TextNode(f"text node: {i}", TextType.TEXT) for i in range(3)]
        results = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertListEqual(results, nodes)

    def test_split_nodes_delimiter_bold(self):
        nodes = [
            TextNode("first text", TextType.TEXT),
            TextNode("**bold** not bold", TextType.TEXT),
            TextNode("last text", TextType.TEXT),
        ]
        expected = [
            TextNode("first text", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" not bold", TextType.TEXT),
            TextNode("last text", TextType.TEXT),
        ]
        results = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(results, expected)

    def test_split_nodes_delimiter_italics(self):
        nodes = [
            TextNode("first text", TextType.TEXT),
            TextNode("_italic_ not italic", TextType.TEXT),
            TextNode("last text", TextType.TEXT),
        ]
        expected = [
            TextNode("first text", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" not italic", TextType.TEXT),
            TextNode("last text", TextType.TEXT),
        ]
        results = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(results, expected)

    def test_split_nodes_delimiter_code(self):
        nodes = [
            TextNode("first text", TextType.TEXT),
            TextNode("`code` not code", TextType.TEXT),
            TextNode("last text", TextType.TEXT),
        ]
        expected = [
            TextNode("first text", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" not code", TextType.TEXT),
            TextNode("last text", TextType.TEXT),
        ]
        results = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(results, expected)

    def test_split_nodes_delimiter_multiple(self):
        nodes = [
            TextNode("first text", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode("bold", TextType.BOLD),
            TextNode("code", TextType.CODE),
            TextNode("_italic first_**then bold**`then code`", TextType.TEXT),
            TextNode("last text", TextType.TEXT),
        ]
        expected_1 = [
            TextNode("first text", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode("bold", TextType.BOLD),
            TextNode("code", TextType.CODE),
            TextNode("italic first", TextType.ITALIC),
            TextNode("**then bold**`then code`", TextType.TEXT),
            TextNode("last text", TextType.TEXT),
        ]
        expected_2 = [
            TextNode("first text", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode("bold", TextType.BOLD),
            TextNode("code", TextType.CODE),
            TextNode("italic first", TextType.ITALIC),
            TextNode("then bold", TextType.BOLD),
            TextNode("`then code`", TextType.TEXT),
            TextNode("last text", TextType.TEXT),
        ]
        expected_3 = [
            TextNode("first text", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode("bold", TextType.BOLD),
            TextNode("code", TextType.CODE),
            TextNode("italic first", TextType.ITALIC),
            TextNode("then bold", TextType.BOLD),
            TextNode("then code", TextType.CODE),
            TextNode("last text", TextType.TEXT),
        ]
        results = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(results, expected_1)
        results = split_nodes_delimiter(results, "**", TextType.BOLD)
        self.assertEqual(results, expected_2)
        results = split_nodes_delimiter(results, "`", TextType.CODE)
        self.assertEqual(results, expected_3)

    def test_split_nodes_delimiter_unclosed_delimiter_error(self):
        nodes = [
            TextNode("first text", TextType.TEXT),
            TextNode("_italic not italic", TextType.TEXT),
            TextNode("last text", TextType.TEXT),
        ]
        args = (nodes, "_", TextType.ITALIC)
        self.assertRaises(ValueError, split_nodes_delimiter, *args)

    def test_extract_markdown_images(self):
        text = (
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
            "This is text with an ![fakeimage](https://fake_img.png)"
        )
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("fakeimage", "https://fake_img.png"),
            ],
            matches,
        )

    def test_extract_markdown_links(self):
        text = (
            "This is text with an [youtube](https://youtube.com)"
            "This is text with an [fakeurl](https://fakeurl.com)"
        )
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("youtube", "https://youtube.com"), ("fakeurl", "https://fakeurl.com")],
            matches,
        )


if __name__ == "__main__":
    unittest.main()
