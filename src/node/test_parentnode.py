import unittest

from node.parentnode import ParentNode
from node.leafnode import LeafNode

props = {
    "href": "https://www.google.com",
    "target": "_blank",
}


class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_children_with_props(self):
        child_node = LeafNode(tag="a", value="child", props=props)
        parent_node = ParentNode("div", [child_node])
        expected_prop = "href='https://www.google.com' target='_blank'"
        self.assertEqual(
            parent_node.to_html(), f"<div><a {expected_prop}>child</a></div>"
        )

    def test_children_with_no_value(self):
        child_node = LeafNode(tag="a", value=None, props=props)
        parent_node = ParentNode("div", [child_node])
        self.assertRaises(ValueError, parent_node.to_html)


if __name__ == "__main__":
    unittest.main()
