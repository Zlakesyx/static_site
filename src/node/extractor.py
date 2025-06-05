import re


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    # ![rick roll](https://i.imgur.com/aKaOqIh.gif)
    pattern = r"\!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    # [youtube](https://www.youtube.com)
    pattern = r"\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)
