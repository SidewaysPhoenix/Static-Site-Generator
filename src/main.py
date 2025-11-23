from textnode import TextNode, TextType
from functions import text_to_textnodes, generate_page
import os
import shutil





def copy_static(source_directory, destination_directory):
    source_list = os.listdir(source_directory)
    for item in source_list:
        source_item_path = os.path.join(source_directory, item)
        destination_item_path = os.path.join(destination_directory, item)
        #if item is a file that does not exist in destination, copy it
        if os.path.isfile(source_item_path):
            shutil.copy(source_item_path, destination_item_path)
        #if item is a directory that does not exist in destination, copy it
        elif os.path.isdir(source_item_path):
            if not os.path.exists(destination_item_path):
                os.mkdir(destination_item_path)
            copy_static(source_item_path, destination_item_path)


def main():
    source_directory = "./static"
    destination_directory = "./public"
    template_path = "./template.html"
    content_path = "./content"
    
    
    if os.path.isdir(destination_directory):
        shutil.rmtree(destination_directory)
    os.mkdir(destination_directory)

    
    copy_static(source_directory, destination_directory)
    generate_page(
        os.path.join(content_path, "index.md"),
        template_path,
        os.path.join(destination_directory, "index.html"),
    )

if __name__ == "__main__":
    main()



#list directories,files in source
#if files are in source directory copy them, if they do not exist in destination_directory yet
#then if first directory in source does not exist make it and then set as current source to go into, otherwise skip and go to next directory to do the same
