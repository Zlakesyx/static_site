import unittest

from block.block_converter import markdown_to_blocks

md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""


class TestBlockConverter(unittest.TestCase):
        def test_markdown_to_blocks(self):
            blocks = markdown_to_blocks(md)
            print(blocks)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )


if __name__ == "__main__":
    unittest.main()
