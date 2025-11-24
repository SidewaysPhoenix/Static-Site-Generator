import os
from markdown_blocks import markdown_to_html_node, markdown_to_blocks

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    with open(from_path, "r") as f:
        markdown_contents = f.read()
    with open(template_path, "r") as f:
        template_contents = f.read()

    html_node = markdown_to_html_node(markdown_contents)
    html_string = html_node.to_html()

    title = extract_title(markdown_contents)

    updated_template_title = template_contents.replace("{{ Title }}", title)
    full_html_page = updated_template_title.replace("{{ Content }}", html_string)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":    
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(full_html_page)



def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block.strip("#").strip()
    raise Exception("No header in markdown")