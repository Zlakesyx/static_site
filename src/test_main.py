import unittest

from main import markdown_to_html_node


class TestSplitter(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = """
# heading 1

## heading 2

### heading 3

#### heading 4

##### heading 5

###### heading 6
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        print("\n" + html)
        self.assertEqual(
            html,
            "<div><h1>heading 1</h1><h2>heading 2</h2><h3>heading 3</h3><h4>heading 4</h4><h5>heading 5</h5><h6>heading 6</h6></div>",
        )

    def test_quote(self):
        md = """
>first line of quote.
>second line of quote.
>third line of quote.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        print("\n" + html)
        self.assertEqual(
            html,
            "<div><blockquote><p>first line of quote. second line of quote. third line of quote.</p></blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- first item
- second item
- third item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        print("\n" + html)
        self.assertEqual(
            html,
            "<div><ul><li>first item</li><li>second item</li><li>third item</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. first item
2. second item
3. third item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        print("\n" + html)
        self.assertEqual(
            html,
            "<div><ol><li>first item</li><li>second item</li><li>third item</li></ol></div>",
        )


if __name__ == "__main__":
    unittest.main()
