import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node, markdown_to_blocks


# old code to pull only one page
def generate_page(from_path, template_path, dest_path, basepath):
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





def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    with open(template_path, "r") as f:
        template_contents = f.read()
    
    content_dir = os.listdir(dir_path_content)
    
    for item in content_dir:
        content_path = (dir_path_content / item)
        dest_dir_new_path = (dest_dir_path / item)
        if os.path.isfile(content_path):
            if content_path.suffix == ".md":
                with open(content_path, "r") as f:
                    markdown_contents = f.read()
                html_node = markdown_to_html_node(markdown_contents)
                html_string = html_node.to_html()

                title = extract_title(markdown_contents)

                title_updated_template = template_contents.replace("{{ Title }}", title)
                content_updated_template = title_updated_template.replace("{{ Content }}", html_string)
                href_updated_template = content_updated_template.replace('href="/', f'href="{basepath}')
                full_html_page = href_updated_template.replace('src="/', f'href="{basepath}')
            
                if dest_dir_path != "":    
                    os.makedirs(dest_dir_path, exist_ok=True)
                with open(dest_dir_new_path.with_suffix(".html"), "w") as f:
                    f.write(full_html_page)
        else:
            generate_pages_recursive(content_path, template_path, dest_dir_new_path, basepath)