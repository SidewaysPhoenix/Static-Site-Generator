from textnode import TextNode, TextType
from functions import text_to_textnodes
import os
import shutil


def main():
    source_directory = "/home/madam/workspace/github.com/bootdev/Static-Site-Generator/static"
    destination_directory = "/home/madam/workspace/github.com/bootdev/Static-Site-Generator/public"


    print(shutil.rmtree(destination_directory))

main()



