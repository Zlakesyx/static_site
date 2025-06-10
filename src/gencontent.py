import os
from markdown_blocks import markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f" * {from_path} {template_path} -> {dest_path}")
    with open(from_path, "r", encoding="utf-8") as from_file:
        markdown_content = from_file.read()

    with open(template_path, "r", encoding="utf-8") as template_file:
        template = template_file.read()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def extract_title(md: str) -> str:
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")
