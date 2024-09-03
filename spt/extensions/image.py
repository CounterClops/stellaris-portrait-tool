import logging
import subprocess
from pathlib import Path

class Image:
    def __init__(self, image_file):
        self.image_file = Path(image_file)

    def crop(self):
        pass
    
    def formatToDds(self, new_file:Path):
        """Formats the image file stored in the class to the DDS format required by Stellaris

        Args:
            new_file (Path): The path to the new filename/location for the DDS file
        """
        command = [
            "magick",
            "-format",
            "dds",
            "-define",
            "dds:compression=dxt5",
            self.image_file,
            new_file
        ]
        try:
            result = subprocess.run(command, check=True, text=True, capture_output=True)
            logging.debug(result)
        except Exception as e:
            logging.error(f"Unable to convert to 'dds': {e}")