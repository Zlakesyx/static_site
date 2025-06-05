import unittest

from node.extractor import (
    extract_markdown_images,
    extract_markdown_links,
)


class TestExtractor(unittest.TestCase):
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
