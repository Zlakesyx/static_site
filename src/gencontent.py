import os
import shutil
from markdown_blocks import markdown_to_html_node


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str
):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        if os.path.isfile(from_path):
            filename, extension = os.path.splitext(filename)
            # Only generate from markdown files
            if extension == ".md":
                dest_path = os.path.join(dest_dir_path, filename + ".html")
                generate_page(from_path, template_path, dest_path, basepath)
        elif os.path.isdir(from_path):
            dest_path = os.path.join(dest_dir_path, filename)
            generate_pages_recursive(from_path, template_path, dest_path, basepath)
        else:
            continue


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str):
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
    template = template.replace("href=\"/", f"href=\"{basepath}")
    template = template.replace("src=\"/", f"src=\"{basepath}")

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
