import os
import copy
import json

####
# I made this because I was lazy and didn't want to have to manually type in each config file, then copy paste names
# It also ensures consistency
# This should be run from the root mod location
# Adjust below paths if not
####

# This should be the relative path to the images, placed in their correct location within the mod folder
relative_portraits_path = "gfx/models/portraits"
# This should be the path to the actual mod folder itself
mod_root_path = os.getcwd()
# This should be the relative location where you'll save the portrait configs
relative_config_output = "gfx/portraits/portraits"

portraits_path = os.path.join(mod_root_path, relative_portraits_path)
config_output = os.path.join(mod_root_path, relative_config_output)

image_list = os.walk(portraits_path)

config_template = {'portraits': {}, 'portrait_groups': {}}
portrait_group_template = {'add':{'portraits':[]}}
config = {}

for path, unknown, file_list in image_list:
    for file in file_list:
        image_path = os.path.join(path, file) # Full path to the image
        mod_image_path = os.path.relpath(image_path, mod_root_path).replace("\\", "/" ) # The relative mod path to the file

        # To create config names, portrait group names etc
        temp_path = os.path.relpath(image_path, portraits_path).lower().replace("\\", "/" ) # Temporary path to generate names
        temp_path_array = temp_path.split("/")

        portrait_group = "pya_" + temp_path_array[0]
        portrait_config = f"{portrait_group}.txt"
        portrait_id = '_'.join(temp_path_array[1:]).split(".")[0] # Generates ID from the file path and name


        # Check defaults
        if portrait_group not in config.keys():
            config[portrait_group] = {'filename': portrait_config, 'content': copy.deepcopy(config_template)}
            config[portrait_group]['content']['portrait_groups'][portrait_group] = {
                'default': portrait_id,
                'game_setup': copy.deepcopy(portrait_group_template),
                'species': copy.deepcopy(portrait_group_template),
                'pop' : copy.deepcopy(portrait_group_template),
                'leader': copy.deepcopy(portrait_group_template),
                'ruler': copy.deepcopy(portrait_group_template)
                }
            
        # Create JSON config      
        config[portrait_group]['content']['portraits'][portrait_id] = {'texturefile' : mod_image_path}
        config[portrait_group]['content']['portrait_groups'][portrait_group]['game_setup']['add']['portraits'].append(portrait_id)
        config[portrait_group]['content']['portrait_groups'][portrait_group]['species']['add']['portraits'].append(portrait_id)
        config[portrait_group]['content']['portrait_groups'][portrait_group]['pop']['add']['portraits'].append(portrait_id)
        config[portrait_group]['content']['portrait_groups'][portrait_group]['leader']['add']['portraits'].append(portrait_id)
        config[portrait_group]['content']['portrait_groups'][portrait_group]['ruler']['add']['portraits'].append(portrait_id)
        

for group_key in config.keys():
    pretty_string = json.dumps(
        config[group_key]['content'],
        sort_keys=False,
        indent=4,
        separators=('', ' = ')
    )
    # Correct minor differences in output string
    replace_array = [['"', ''], ['gfx', '"gfx'], ['.dds', '.dds"'], ['[', '{'], [']', '}']]
    for replacement in replace_array:
        pretty_string = pretty_string.replace(*replacement)
    pretty_string = pretty_string.split('{\n',1)[1].rsplit('}',1)[0]

    # Remove extra indent at the start of the lines after removing outter {} brackets
    lines = []
    for line in pretty_string.splitlines():
        lines.append(line[4:])
    pretty_string = '\n'.join(lines)

    # Save file
    with open(os.path.join(config_output, config[group_key]['filename']), "w") as config_file:
        config_file.write(pretty_string)
    
