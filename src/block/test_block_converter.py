import unittest

from block.block_converter import block_to_block_type, markdown_to_blocks, BlockType

md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

blocks = [
    "This is **bolded** paragraph",
    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
    "- This is a list\n- with items",
]


class TestBlockConverter(unittest.TestCase):
    def test_markdown_to_blocks(self):
        self.assertEqual(markdown_to_blocks(md), blocks)

        # return BlockType.UNORDERED_LIST
        # return BlockType.ORDERED_LIST

    def test_block_to_heading(self):
        inputs = [
            "# heading",
            "## heading",
            "### heading",
            "#### heading",
            "##### heading",
            "###### heading",
        ]
        # too many #
        not_heading = "####### not heading"
        for input in inputs:
            self.assertEqual(block_to_block_type(input), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type(not_heading), BlockType.HEADING)

    def test_block_to_code(self):
        inputs = [
            "``` this is a code block ```",
            "```this is a code block```",
        ]
        not_code = [
            "not code```this is not a code block```",
            "```this is not a code block``` not code",
        ]
        for input in inputs:
            self.assertEqual(block_to_block_type(input), BlockType.CODE)
        for input in not_code:
            self.assertNotEqual(block_to_block_type(input), BlockType.CODE)

    def test_block_to_quote(self):
        inputs = [
            "> quote",
            "> quote\n>quote",
        ]
        not_quote = [
            "!> quote",
            "\n> quote\n>quote",
        ]
        for input in inputs:
            self.assertEqual(block_to_block_type(input), BlockType.QUOTE)
        for input in not_quote:
            self.assertNotEqual(block_to_block_type(input), BlockType.QUOTE)

    def test_block_to_unordered_list(self):
        inputs = [
            "- item",
            "- item\n- item",
        ]
        not_unorderd_list = [
            "!- item",
            "\n- item\n-item",
        ]
        for input in inputs:
            self.assertEqual(block_to_block_type(input), BlockType.UNORDERED_LIST)
        for input in not_unorderd_list:
            self.assertNotEqual(block_to_block_type(input), BlockType.UNORDERED_LIST)

    def test_block_to_ordered_list(self):
        inputs = [
            "1. item",
            "1. item\n2. item",
        ]
        not_unorderd_list = [
            "2. item",
            "-1. item\n2. item",
        ]
        for input in inputs:
            self.assertEqual(block_to_block_type(input), BlockType.ORDERED_LIST)
        for input in not_unorderd_list:
            self.assertNotEqual(block_to_block_type(input), BlockType.ORDERED_LIST)

    def test_block_to_paragraph(self):
        paragraph = blocks[1]
        self.assertEqual(block_to_block_type(paragraph), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
