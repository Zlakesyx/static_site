import unittest

from node.leafnode import LeafNode
from node.textnode import TextNode, TextType
from main import text_node_to_html_node

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


if __name__ == "__main__":
    unittest.main()
