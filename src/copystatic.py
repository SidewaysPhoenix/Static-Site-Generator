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