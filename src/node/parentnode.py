from node.htmlnode import HTMLNode
from node.leafnode import LeafNode


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: list[LeafNode], props: dict[str, str] = None
    ) -> None:
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("All parent nodes must have a tag")

        html_str = f"<{self.tag}"
        if self.props:
            html_str += f" {self.props_to_html()}"
        html_str += ">"

        for child in self.children:
            html_str += child.to_html()

        html_str += f"</{self.tag}>"
        return html_str

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}, {self.tag}, {self.children}, {self.props}"
