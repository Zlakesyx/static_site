class HTMLNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list["HTMLNode"] = None,
        props: dict[str, str] = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        html_str = ""
        for k, v in self.props.items():
            html_str += f"{k}='{v}' "
        return html_str.strip()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}, {self.tag}, {self.value}, {self.children}, {self.props}"
