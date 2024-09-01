import logging
import subprocess
from pathlib import Path
import copy
import json
import re

import templates

class Portraits:
    def __init__(self, source_path, mod_prefix:str=""):
        self.source_path = Path(source_path)
        self.image_root_path = self.source_path / Path("gfx/models/portraits")
        self.config_root_path = self.source_path / Path("gfx/portraits/portraits")
        self.config_store = {}
        self.mod_prefix = mod_prefix
    
    @staticmethod
    def replaceKeySeperators(key_string) -> str:
        for string in ["/", "\\"]:
            seperator = "_"
            key_string = key_string.replace(string, seperator)
        return key_string

    @staticmethod
    def removeQuotes(string) -> str:
        if string.startswith("[") and string.endswith("]"):
            return string

        return string.replace('"', '').replace("'", '')
    
    @staticmethod
    def convertJsonToConfig(string) -> str:
        replace_array = [
            ['[', '{'], 
            [']', '}']
        ]
        for replacement in replace_array:
            string = string.replace(*replacement)
        
        string = string.split('{\n',1)[1].rsplit('}',1)[0]

        # Remove extra indent at the start of the lines after removing outter {} brackets
        lines = []
        for line in string.splitlines():
            lines.append(line[4:])
        string = '\n'.join(lines)

        return string

    def createGroupKey(self, file) -> str:
        image_relative_path = file.relative_to(self.image_root_path)
        group_key = str(image_relative_path.parent)
        group_key = self.replaceKeySeperators(group_key)
        if self.mod_prefix != "":
            group_key = "_".join([self.mod_prefix, group_key])
        return group_key

    def createVariantPrefix(self, file) -> str:
        image_relative_path = file.relative_to(self.image_root_path)

        if (len(image_relative_path.parents)) <= 2:
            return ""
        
        # The below creates the variant prefix which is any sub folder under each portrait folder
        variant_prefix = str(image_relative_path.parent)
        variant_prefix = self.replaceKeySeperators(variant_prefix)
        variant_prefix = variant_prefix.split("_", 1)[1]

        return variant_prefix

    def generateConfigs(self):
        for file in self.image_root_path.rglob("*.dds"):
            image_relative_path = file.relative_to(self.source_path)
            group_key = self.createGroupKey(file=file)
            variant_prefix = self.createVariantPrefix(file=file)

            if variant_prefix != "":
                image_ref = "_".join([variant_prefix, file.stem])
            else:
                image_ref = file.stem

            if self.mod_prefix != "":
                config_filename = f"{self.mod_prefix}_{group_key}.txt"
            else:
                config_filename = f"{group_key}.txt"

            if group_key not in self.config_store.keys():
                self.config_store[group_key] = {'filename': config_filename, 'content': copy.deepcopy(templates.Portraits.root_config)}
                self.config_store[group_key]['content']['portrait_groups'][group_key] = {
                    'default': image_ref,
                    'game_setup': copy.deepcopy(templates.Portraits.portrait_group),
                    'species': copy.deepcopy(templates.Portraits.portrait_group),
                    'pop' : copy.deepcopy(templates.Portraits.portrait_group),
                    'leader': copy.deepcopy(templates.Portraits.portrait_group),
                    'ruler': copy.deepcopy(templates.Portraits.portrait_group)
                }

            self.config_store[group_key]['content']['portraits'][image_ref] = {'texturefile': str(image_relative_path)}
            self.config_store[group_key]['content']['portrait_groups'][group_key]['game_setup']['add']['portraits'].append(image_ref)
            self.config_store[group_key]['content']['portrait_groups'][group_key]['species']['add']['portraits'].append(image_ref)
            self.config_store[group_key]['content']['portrait_groups'][group_key]['pop']['add']['portraits'].append(image_ref)
            self.config_store[group_key]['content']['portrait_groups'][group_key]['leader']['add']['portraits'].append(image_ref)
            self.config_store[group_key]['content']['portrait_groups'][group_key]['ruler']['add']['portraits'].append(image_ref)

    def dumpConfigs(self):
        pattern = re.compile(r'(\[[^\]]*\])') 

        for group_key in self.config_store.keys():
            logging.info(f"Creating config for '{group_key}'")
            pretty_config = json.dumps(
                self.config_store[group_key]['content'],
                sort_keys=False,
                indent=4,
                separators=('', ' = ')
            )
            config_parts = pattern.split(pretty_config)
            config_parts = [self.removeQuotes(part) for part in config_parts]
            pretty_config = "".join(config_parts)
            pretty_config = self.convertJsonToConfig(pretty_config)
        
            config_filename = self.config_store[group_key]['filename']
            config_filepath = self.config_root_path / config_filename

            logging.info(f"Saving '{config_filepath}'")
            config_filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(config_filepath, "w") as config_file:
                config_file.write(pretty_config)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,  # Set the minimum logging level
        format='%(levelname)s: %(message)s',  # Set the log message format
        handlers=[logging.StreamHandler()]  # Output to the terminal
    )
    sp = Portraits(source_path="/home/counter/Downloads/Stellaris/output2")
    sp.generateConfigs()
    sp.dumpConfigs()