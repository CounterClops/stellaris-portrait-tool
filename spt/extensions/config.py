import logging
from pathlib import Path
import json
import sys

from . import templates

# https://pdx.tools/blog/a-tour-of-pds-clausewitz-syntax

class Configs:
    def __init__(self, source_path, mod_prefix:str="", conflict_resolution_method:str="stop", species_archetype:str="BIOLOGICAL"):
        self.source_path = Path(source_path)
        self.config_store = {
            # Example
            # group_id: {
            #     'filename': "filename.txt", 
            #     'content': {}
            # }
        }
        self.mod_prefix = mod_prefix
        self.conflict_resolution_method = conflict_resolution_method
        self.species_archetype = species_archetype
        self.quoted_value_keys = []
        try:
            self.setup()
        except AttributeError as e:
            logging.debug(f"Setup function error (Setup function may not exist) {e}")
    
    def setup(self):
        """Should be replaced by child class inheriting this parent class. This function defines any required setup for the child class, and should be considered an expansion on __init__
        """
        logging.error(f"{self.__class__} does not contain a proper setup() function")

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
    def replaceSquareBrackets(string:str) -> str:
        """Replaces all [] with {} characters in the provided string

        Args:
            string (str): The string to clear of [] characters

        Returns:
            str: The string with only {} characters
        """
        replace_array = [
            ['[', '{'], 
            [']', '}']
        ]
        for replacement in replace_array:
            string = string.replace(*replacement)
        
        return string

    @staticmethod
    def checkRequiredQuotes(string:str) -> bool:
        """Check if the provided string has any characters that require the string remain quoted

        Args:
            string (str): The string to check

        Returns:
            bool: Whether the string should be kept quoted
        """
        quote_required_characters = [
            " ",
            "/",
            "\\"
        ]
        # if not any(substring in string.strip(" ") for substring in quote_required_characters):
        #     # string = self.removeQuotes(string)
        quotes_required = any(substring in string.strip(" ") for substring in quote_required_characters)

        return quotes_required

    def removeQuotes(self, string:str) -> str:
        """Remove all quotes where allowed in the provided string

        Args:
            string (str): The string to clear of quote characters where allowed

        Returns:
            str: The cleaned string
        """
        replace_array = [
            ['"', ''], 
            ["'", '']
        ]
        if self.checkRequiredQuotes(string=string):
            return string
        
        for replacement in replace_array:
            string = string.replace(*replacement)
        
        return string

    def checkQuotedValueKey(self, key:str) -> bool:
        """Check if the provided key should have its value kept inside of a quote

        Args:
            key (str): The key to check against the internal self.quoted_value_keys list

        Returns:
            bool: Whether the key is for a value that should remain quoted
        """
        trimmed_key = self.removeQuotes(key.strip())
        if trimmed_key in self.quoted_value_keys:
            return True
        return False

    def cleanConfig(self, string:str) -> str:
        """Converts the python dict to a format closer to what Stellaris requires in its config

        Args:
            string (str): The python dict as a pretty printed string

        Returns:
            str: The cleaned config as a string
        """
        # Replace square brackets with curly
        string = self.replaceSquareBrackets(string)

        # Remove leading/trailing curly brackets
        string = string.split('{\n',1)[1].rsplit('}',1)[0]

        # Remove quotes on all leading variable names etc
        lines = string.splitlines()

        cleaned_lines = []
        for line in lines:
            if "=" not in line:
                cleaned_lines.append(self.removeQuotes(line)[4:])
                continue
            
            line_parts = line.split("=")
            new_parts = []
            for part in line_parts[:-1]:
                new_parts.append(self.removeQuotes(part))

            potential_key = new_parts[0]
            last_part = line_parts[-1]
            if not self.checkQuotedValueKey(key=potential_key):
                new_parts.append(self.removeQuotes(last_part))
            else:
                new_parts.append(last_part)
        
            cleaned_lines.append("=".join(new_parts)[4:])

        string = "\n".join(cleaned_lines)

        return string
    
    def createSpeciesClassName(self):
        species_class_name = "_".join([
            self.mod_prefix,
            self.species_archetype.lower(),
            "class"
        ])
        return species_class_name

    def createSpeciesNameName(self):
        species_class_name = "_".join([
            self.mod_prefix,
            self.species_archetype.lower(),
            "name"
        ])
        return species_class_name

    def createPortraitSetName(self):
        portrait_set_name = "_".join([
            self.mod_prefix,
            self.species_archetype.lower(),
            "set"
        ])
        return portrait_set_name

    def createPortraitCategoryName(self):
        portrait_category_name = "_".join([
            self.mod_prefix,
            self.species_archetype.lower(),
            "category"
        ])
        return portrait_category_name

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
            group_key = "_".join([
                self.mod_prefix, 
                group_key
            ])
        return group_key

    def dumpConfigs(self):
        """Converts the stored configs in this class to pretty printed JSON, which are then converted to Stellaris PDX clausewitz format
        """

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
                        logging.error(f"File conflict: '{config_filepath}' already exists, stopping execution. Check --help if you'd like files to be overrode")
                        sys.exit(1)
                    case "skip":
                        logging.debug(f"File conflict: '{config_filepath}' already exists, skipping")
                        continue
            
            logging.info(f"Saving '{group_key}' config to '{config_filepath}'")
            config_filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(config_filepath, "w") as config_file:
                config_file.write(pretty_config)

    def generateConfigs(self):
        """Should be replaced by child class inheriting this parent class. This function will typically generate the configs as dicts and store them in the config_store dict
        """
        logging.error(f"{self.__class__} does not contain a proper generateConfigs() function")

    def generate(self):
        """Basic function to run the generation and config dump in a single call
        """
        self.generateConfigs()
        self.dumpConfigs()

class Portraits(Configs):
    def setup(self):
        self.image_root_path = self.source_path / Path("gfx/models/portraits")
        self.config_root_path = self.source_path / Path("gfx/portraits/portraits")
        self.quoted_value_keys = [
            "texturefile"
        ]

    def generateConfigs(self):
        """Generates the Configs which are stored under each group_key in the config_store of this class
        """

        portrait_files = {}

        for file in self.image_root_path.rglob("*.dds"):
            image_relative_path = file.relative_to(self.source_path)
            portrait_group_name = self.createGroupKey(file=file)
            variant_prefix = self.createVariantPrefix(file=file)

            if variant_prefix != "":
                image_ref = "_".join([variant_prefix, file.stem])
            else:
                image_ref = file.stem
            
            try:
                portrait_files[portrait_group_name]
            except:
                portrait_files[portrait_group_name] = {}

            portrait_files[portrait_group_name][image_ref] = {
                "texturefile": str(image_relative_path)
            }
        
        for portrait_group_name in portrait_files.keys():
            portrait_refs = list(portrait_files[portrait_group_name].keys())
            portraits = templates.Portraits(
                portrait_group_name = portrait_group_name,
                portrait_refs = portrait_refs,
                portrait_files = portrait_files[portrait_group_name]
            )

            config_filename = f"{portrait_group_name}.txt"
            self.config_store[portrait_group_name] = {
                'filename': config_filename, 
                'content': portraits.config
            }

class PortraitSets(Configs):
    def setup(self):
        self.config_root_path = self.source_path / Path("common/portrait_sets")
        self.config_portraits_path = self.source_path / Path("gfx/portraits/portraits")
    
    def generateConfigs(self):
        portrait_set_name = self.createPortraitSetName()
        species_class_name = self.createSpeciesClassName()

        portrait_configs = []

        for file in self.config_portraits_path.rglob("*.txt"):
            config_ref = file.stem
            portrait_configs.append(config_ref)
        
        portrait_sets = templates.PortraitSets(
            portrait_set_name=portrait_set_name,
            species_class_name=species_class_name,
            portraits=portrait_configs
        )

        config_filename = f"{portrait_set_name}.txt"

        self.config_store[portrait_set_name] = {
            'filename': config_filename, 
            'content': portrait_sets.config
        }

class SpeciesClass(Configs):
    def setup(self):
        self.config_root_path = self.source_path / Path("common/species_classes")
    
    def generateConfigs(self):
        species_class_name = self.createSpeciesClassName()

        species_class = templates.SpeciesClass(
            species_class_name=species_class_name,
            archetype=self.species_archetype
        )

        config_filename = f"{species_class_name}.txt"

        self.config_store[species_class_name] = {
            'filename': config_filename, 
            'content': species_class.config
        }

class SpeciesNames(Configs):
    def setup(self):
        self.config_root_path = self.source_path / Path("common/species_names")
        self.quoted_value_keys = [
            "name_list"
        ]

    def generateConfigs(self):
        species_class_name = self.createSpeciesClassName()
        species_name_name = self.createSpeciesNameName()

        species_class = templates.SpeciesNames(
            species_class_name=species_class_name,
            archetype=self.species_archetype
        )

        config_filename = f"{species_name_name}.txt"

        self.config_store[species_name_name] = {
            'filename': config_filename, 
            'content': species_class.config
        }

class PortraitCategories(Configs):
    def setup(self):
        self.config_root_path = self.source_path / Path("common/portrait_categories")
        self.config_portraits_path = self.source_path / Path("gfx/portraits/portraits")
    
    def generateConfigs(self):
        portrait_category_name = self.createPortraitCategoryName()
        portrait_set_name = self.createPortraitSetName()

        portrait_categorys = templates.PortraitCategories(
            category_name=portrait_category_name,
            portrait_sets=[portrait_set_name]
        )

        config_filename = f"{portrait_category_name}.txt"

        self.config_store[portrait_category_name] = {
            'filename': config_filename, 
            'content': portrait_categorys.config
        }