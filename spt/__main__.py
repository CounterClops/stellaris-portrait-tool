import argparse
from pathlib import Path
import logging
from spt import StellarisPortraitTool

def setup_logger():
    # Create a logger object
    logging.basicConfig(
        level=logging.INFO,  # Set the minimum logging level
        format='%(levelname)s: %(message)s',  # Set the log message format
        handlers=[logging.StreamHandler()]  # Output to the terminal
    )

if __name__ == "__main__":
    logger = setup_logger()

    parser = argparse.ArgumentParser(
        prog="Stellaris Portrait Tool",
        description="Tool used to generate stellaris configs, and convert images to the required formats",
        epilog="Source: https://github.com/CounterClops/stellaris-portrait-tool"
    )
    parser.add_argument(
        "-s",
        "--source-folder",
        dest="source_folder",
        required=True,
        type=Path,
        help="The source folder containing all files/subfolders"
    )
    parser.add_argument(
        "-o",
        "--output-folder",
        dest="output_folder",
        required=True,
        type=Path,
        help="The location to output all new files"
    )
    parser.add_argument(
        "--file-conflict",
        dest="conflict_resolution_method",
        choices=["replace", "stop", "skip"],
        default="stop",
        type=str,
        help="The location to output all new files"
    )
    parser.add_argument(
        "--skip-image-convert",
        dest="skip_image_convert",
        action="store_true",
        help="Do not convert any images"
    )

    args = parser.parse_args()

    spt = StellarisPortraitTool(
        source_folder = args.source_folder,
        output_folder = args.output_folder,
        conflict_resolution_method = args.conflict_resolution_method,
    )
    
    if not args.skip_image_convert:
        spt.bulkConvertImages()
