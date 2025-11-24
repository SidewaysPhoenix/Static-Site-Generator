import os
import shutil

from copystatic import copy_static
from gencontent import generate_page

source_directory = "./static"
destination_directory = "./public"
template_path = "./template.html"
content_path = "./content"

def main():

    print("Deleting public directory...")
    if os.path.exists(destination_directory):
        shutil.rmtree(destination_directory)
    os.mkdir(destination_directory)

    print("Copying static files to public directory...")
    copy_static(source_directory, destination_directory)
    
    print("Generating page...")
    generate_page(
        os.path.join(content_path, "index.md"),
        template_path,
        os.path.join(destination_directory, "index.html"),
    )


main()



#list directories,files in source
#if files are in source directory copy them, if they do not exist in destination_directory yet
#then if first directory in source does not exist make it and then set as current source to go into, otherwise skip and go to next directory to do the same
