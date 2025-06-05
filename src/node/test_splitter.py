import unittest

from node.textnode import TextNode, TextType
from node.splitter import (
    split_nodes_delimiter,
    split_nodes_images,
    split_nodes_links,
    text_to_nodes,
)


class TestSplitter(unittest.TestCase):
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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_single(self):
        nodes = [
            TextNode(
                "This is text with an [link](https://youtube.com) and another [second link](https://youtube.com/second)",
                TextType.TEXT,
            )
        ]
        new_nodes = split_nodes_links(nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://youtube.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://youtube.com/second"),
            ],
            new_nodes,
        )

    def test_split_links_multiple(self):
        nodes = [
            TextNode(
                "This is text with an [link](https://youtube.com) and another [second link](https://youtube.com/second)",
                TextType.TEXT,
            ),
            TextNode("link", TextType.LINK, "https://youtube.com"),
            TextNode(
                "last link [last link](http://lastlink.com)",
                TextType.TEXT,
            ),
        ]
        new_nodes = split_nodes_links(nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://youtube.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://youtube.com/second"),
                TextNode("link", TextType.LINK, "https://youtube.com"),
                TextNode("last link ", TextType.TEXT),
                TextNode("last link", TextType.LINK, "http://lastlink.com"),
            ],
            new_nodes,
        )

    def test_split_links_none(self):
        nodes = [
            TextNode(
                "This is text",
                TextType.TEXT,
            )
        ]
        new_nodes = split_nodes_links(nodes)
        self.assertListEqual(
            [
                TextNode("This is text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_nodes(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and "
            "an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and "
            "a [link](https://boot.dev)"
        )
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(text_to_nodes(text), expected)


if __name__ == "__main__":
    unittest.main()
