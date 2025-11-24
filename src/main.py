import os
import shutil

from pathlib import Path
from copystatic import copy_static
from gencontent import generate_page, generate_pages_recursive

source_directory = "./static"
destination_directory = Path("./public")
template_path = "./template.html"
content_path = Path("./content")

def main():

    print("Deleting public directory...")
    if os.path.exists(destination_directory):
        shutil.rmtree(destination_directory)
    os.mkdir(destination_directory)

    print("Copying static files to public directory...")
    copy_static(source_directory, destination_directory)
    
    print("Generating page...")
    
    #    Old Code
    #generate_page(
    #    os.path.join(content_path, "index.md"),
    #    template_path,
    #    os.path.join(destination_directory, "index.html"),
    #)
    generate_pages_recursive(
        content_path,
        template_path,
        destination_directory,
    )


main()



