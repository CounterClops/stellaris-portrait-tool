import os
import copy
import json

# https://wiki.python.org/moin/ImageMagick

# convert -format dds -define dds:compression=dxt5 temp.png temp.dds

source_folder = "source"
output_folder = "output"
convert_cmd = 'convert -format dds -define dds:compression=dxt5 "{source_file}" "{output_file}"'
#convert_cmd = 'convert -format png "{source_file}" "{output_file}"'

old_extension = ".png"
new_extension = ".dds"

current_path = os.getcwd()

source_folder = os.path.join(current_path, source_folder)
output_folder = os.path.join(current_path, output_folder)

image_list = os.walk(source_folder)

for path, unknown, file_list in image_list:
    for file in file_list:
        # Image path
        source_image_path = os.path.join(path, file)
        relative_path = os.path.relpath(source_image_path, source_folder).replace("\\", "/" )
        
        # Folder path array
        temp_path = os.path.relpath(source_image_path, source_folder).lower().replace("\\", "/" ) # Temporary path to generate names
        temp_path_array = temp_path.split("/")

        # Create mirror folder structure in the output folder
        output_sub_folder = os.path.join(output_folder, *temp_path_array[:-1])
        os.makedirs(output_sub_folder, exist_ok = True)

        # New file info
        output_file = os.path.join(output_folder, relative_path).replace(old_extension, new_extension)

        # Run the convert command
        os.popen(convert_cmd.format(source_file=source_image_path, output_file=output_file)).read()
