import logging
from pathlib import Path
import copy
import json
import re
import sys

from . import templates

# https://pdx.tools/blog/a-tour-of-pds-clausewitz-syntax

class Portraits:
    def __init__(self, source_path, mod_prefix:str="", conflict_resolution_method:str="stop"):
        self.source_path = Path(source_path)
        self.image_root_path = self.source_path / Path("gfx/models/portraits")
        self.config_root_path = self.source_path / Path("gfx/portraits/portraits")
        self.config_store = {}
        self.mod_prefix = mod_prefix
        self.conflict_resolution_method = conflict_resolution_method
    
    @staticmethod
    def replaceKeySeperators(key_string:str) -> str:
        """Replace seperators in keys with _ characters

        Args:
            key_string (str): The key to have its seperators replaced

        Returns:
            str: The key with all seperators replaced
        """
        for string in ["/", "\\", " ", "-"]:
            seperator = "_"
            key_string = key_string.replace(string, seperator)
        return key_string

    @staticmethod
    def cleanConfig(string:str) -> str:
        """Converts the python dict to a format closer to what Stellaris requires in its config

        Args:
            string (str): The python dict as a pretty printed string

        Returns:
            str: The cleaned config as a string
        """
        # Replace square brackets with curly
        replace_array = [
            ['[', '{'], 
            [']', '}']
        ]
        for replacement in replace_array:
            string = string.replace(*replacement)

        # Remove leading/trailing curly brackets
        string = string.split('{\n',1)[1].rsplit('}',1)[0]

        # Remove quotes on all leading variable names etc
        lines = string.splitlines()

        cleaned_lines = []
        for line in lines:
            line_parts = line.split("=")
            if "=" not in line:
                cleaned_lines.append(line.replace('"', '').replace("'", ''))
                continue
            line_parts = line.split("=")
            new_parts = []
            for part in line_parts[:-1]:
                new_parts.append(part.replace('"', '').replace("'", ''))
            new_parts.append(line_parts[-1])
        
            cleaned_lines.append("=".join(new_parts)[4:])

        string = "\n".join(cleaned_lines)

        return string

    def createGroupKey(self, file:Path) -> str:
        """Create a group key based on the file path

        Args:
            file (Path): The group key for the specific file

        Returns:
            str: The generated group key
        """
        image_relative_path = file.relative_to(self.image_root_path)
        group_key = str(image_relative_path.parent)
        group_key = self.replaceKeySeperators(group_key)
        if self.mod_prefix != "":
            group_key = "_".join([self.mod_prefix, group_key])
        return group_key

    def createVariantPrefix(self, file:Path) -> str:
        """Creates a variant prefix to be used to denote sub classes of a species

        Args:
            file (Path): The file you'd like generate the variant prefix for

        Returns:
            str: The variant prefix
        """
        image_relative_path = file.relative_to(self.image_root_path)

        if (len(image_relative_path.parents)) <= 2:
            return ""
        
        # The below creates the variant prefix which is any sub folder under each portrait folder
        variant_prefix = str(image_relative_path.parent)
        variant_prefix = self.replaceKeySeperators(variant_prefix)
        variant_prefix = variant_prefix.split("_", 1)[1]

        return variant_prefix

    def generateConfigs(self):
        """Generates the Configs which are stored under each group_key in the config_store of this class
        """
        for file in self.image_root_path.rglob("*.dds"):
            image_relative_path = file.relative_to(self.source_path)
            group_key = self.createGroupKey(file=file)
            variant_prefix = self.createVariantPrefix(file=file)

            if variant_prefix != "":
                image_ref = "_".join([variant_prefix, file.stem])
            else:
                image_ref = file.stem

            if self.mod_prefix != "":
                config_filename = f"{group_key}.txt"
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
        """Converts the stored configs in this class to pretty printed JSON, which are then converted to Stellaris PDX clausewitz format
        """
        pattern = re.compile(r'(\[[^\]]*\])')

        for group_key in self.config_store.keys():
            logging.debug(f"Creating config for '{group_key}'")
            pretty_config = json.dumps(
                self.config_store[group_key]['content'],
                sort_keys=False,
                indent=4,
                separators=('', ' = ')
            )

            pretty_config = self.cleanConfig(string=pretty_config)
        
            config_filename = self.config_store[group_key]['filename']
            config_filepath = self.config_root_path / config_filename

            if config_filepath.is_file():
                match self.conflict_resolution_method:
                    case "stop":
                        logging.error(f"File conflict: '{config_filepath}' already exists, stopping execution")
                        sys.exit(1)
                    case "skip":
                        logging.debug(f"File conflict: '{config_filepath}' already exists, skipping")
                        continue
            
            logging.info(f"Saving '{group_key}' config to '{config_filepath}'")
            config_filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(config_filepath, "w") as config_file:
                config_file.write(pretty_config)

    def generate(self):
        """Basic function to run the generation and config dump in a single call
        """
        self.generateConfigs()
        self.dumpConfigs()