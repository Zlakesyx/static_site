from enum import Enum


class TextType(str, Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: "TextNode") -> bool:
        return all(
            [
                self.text == other.text,
                self.text_type == other.text_type,
                self.url == other.url,
            ]
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.text}, {self.text_type.value}, {self.url})"
