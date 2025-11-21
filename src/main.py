from textnode import TextNode, TextType
from functions import text_to_textnodes
import os
import shutil


def main():

    source_directory = "/home/madam/workspace/github.com/bootdev/Static-Site-Generator/static"
    destination_directory = "/home/madam/workspace/github.com/bootdev/Static-Site-Generator/public"
    #clear destination
    shutil.rmtree(destination_directory)
    #remake destination
    os.mkdir(destination_directory)
    def copy_static(source_directory, destination_directory):
        source_list = os.listdir(source_directory)
        for item in source_list:
            source_item_path = os.path.join(source_directory, item)
            destination_item_path = os.path.join(destination_directory, item)
            #if item is a file that does not exist in destination, copy it
            if os.path.isfile(source_item_path):
                shutil.copy(source_item_path, destination_directory)
            #if item is a directory that does not exist in destination, copy it
            elif os.path.isdir(source_item_path):
                os.mkdir(destination_item_path)
                copy_static(source_item_path, destination_item_path)

    copy_static(source_directory,destination_directory)
main()



#list directories,files in source
#if files are in source directory copy them, if they do not exist in destination_directory yet
#then if first directory in source does not exist make it and then set as current source to go into, otherwise skip and go to next directory to do the same
