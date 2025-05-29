import unittest

from node.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_eq(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(props=props)
        result = node.props_to_html()
        expected = "href='https://www.google.com' target='_blank'"

        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
