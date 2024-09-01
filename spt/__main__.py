import argparse
from pathlib import Path
import logging
from spt import StellarisPortraitTool

def setup_logger(mode:str="INFO"):
    # Create a logger object
    match mode:
        case "INFO":
            logging_mode=logging.INFO
        case "DEBUG":
            logging_mode=logging.DEBUG
        case "WARNING":
            logging_mode=logging.WARNING
        case "ERROR":
            logging_mode=logging.ERROR
        case _:
            logging_mode=logging.INFO
    
    logging.basicConfig(
        level=logging_mode,  # Set the minimum logging level
        format='%(levelname)s: %(message)s',  # Set the log message format
        handlers=[logging.StreamHandler()]  # Output to the terminal
    )

if __name__ == "__main__":
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
    parser.add_argument(
        "--logging",
        dest="logging",
        choices=["INFO", "WARNING", "ERROR", "DEBUG"],
        default="INFO",
        help="Logging mode to use"
    )
    parser.add_argument(
        "-g",
        "--generate-configs",
        dest="generate_configs",
        action="store_true",
        help="Generate configs for matching files"
    )

    args = parser.parse_args()

    logger = setup_logger(mode=args.logging)

    spt = StellarisPortraitTool(
        source_folder = args.source_folder,
        output_folder = args.output_folder,
        conflict_resolution_method = args.conflict_resolution_method,
    )
    
    if not args.skip_image_convert:
        spt.bulkConvertImages()
