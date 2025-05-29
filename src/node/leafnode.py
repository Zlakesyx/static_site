from node.htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict[str, str] = None) -> None:
        self.tag = tag
        self.value = value
        self.props = props
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return self.value

        html_str = f"<{self.tag}"
        if self.props:
            html_str += f" {self.props_to_html()}"
        html_str += f">{self.value}</{self.tag}>"

        return html_str
