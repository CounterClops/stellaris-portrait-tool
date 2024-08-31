import sys
import logging
from pathlib import Path
import subprocess
from extensions import image

class StellarisPortraitTool:
    def __init__(self, source_folder="source", output_folder="output", conflict_resolution_method="stop"):
        self.source_folder = Path(source_folder)
        self.output_folder = Path(output_folder)
        self.conflict_resolution_method = conflict_resolution_method
        self.accepted_image_extensions = [".png"]

        if not self.checkDependencies():
            sys.exit(1)
        if not self.checkPaths():
            sys.exit(1)

    @staticmethod
    def checkDependencies():
        try:
            command = ["magick", "--version"]
            result = subprocess.run(command, check=True, text=True, capture_output=True)
            logging.debug(result)
        except Exception as e:
            logging.error(f"Missing ImageMagick dependency: {e}")
            logging.error(f"Please install ImageMagick to your system path: https://imagemagick.org/")
        return True
    
    def checkPaths(self):
        # Source folder check
        valid_source = (
            self.source_folder.exists() 
            and 
            self.source_folder.is_dir()
        )
        if not valid_source:
            logging.error(f"'{self.source_folder}' source folder either does not exist, or is not a directory")
            return False
        
        # Output folder check
        self.output_folder.mkdir(parents=True, exist_ok=True)
        return True
    
    def bulkConvertImages(self):
        new_image_extension = ".dds"
        
        for file in self.source_folder.rglob('*'):
            relative_path = file.relative_to(self.source_folder)
            new_path = self.output_folder / relative_path
            new_file = new_path.with_suffix(new_image_extension)

            if not file.is_file():
                new_path.mkdir(parents=True, exist_ok=True)
                continue

            file_extension= file.suffix.lower()
            if not file_extension in self.accepted_image_extensions:
                logging.debug(f"Skipping file '{file}' as not accepted")
                continue

            if new_file.is_file():
                match self.conflict_resolution_method:
                    case "stop":
                        logging.error(f"File conflict: '{file}' already exists, stopping execution")
                        sys.exit(1)
                    case "skip":
                        logging.debug(f"File conflict: '{file}' already exists, skipping")
                        continue

            logging.info(f"Converting '{file}' to '{new_file}'")
            
            image_object = image.Image(
                image_file = file
            )

            image_object.formatToDds(
                new_file = new_file
            )

    def bulkGenerateConfigs(self):
        # Loop over files in output folder
        # For each file with a matching ext continue
        # Generate Stellaris configs for portraits
        pass