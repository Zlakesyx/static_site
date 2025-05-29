import unittest

from leafnode import LeafNode

props = {
    "href": "https://www.google.com",
    "target": "_blank",
}

value = "Hello!"


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", value)
        self.assertEqual(node.to_html(), f"<p>{value}</p>")

    def test_leaf_to_html_p_with_props(self):
        node = LeafNode("p", value, props)
        expected_prop = "href='https://www.google.com' target='_blank'"
        self.assertEqual(node.to_html(), f"<p {expected_prop}>{value}</p>")

    def test_no_tag(self):
        node = LeafNode(tag=None, value=value, props=props)
        self.assertEqual(node.to_html(), value)

    def test_no_value(self):
        node = LeafNode(tag="a", value=None, props=props)
        self.assertRaises(ValueError, node.to_html)


if __name__ == "__main__":
    unittest.main()
