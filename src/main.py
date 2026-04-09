from pathlib import Path
import argparse
import sys
from src.annotation_controller import AnnotationController

def main():
    parser = argparse.ArgumentParser(description='Annotator - A tool for annotating human pose datasets.')
    parser.add_argument('data_path', type=str, help='Path to the data to be annotated.')
    parser.add_argument('json_path', type=str, help='Path to the json-file/folder to save annotations.' )
    parser.add_argument('--video_mode', action='store_true', help='Enable video mode for annotation.')

    args = parser.parse_args()

    if not Path(args.data_path).exists():
        print(f"Error: The path '{args.data_path}' does not exist!")
        sys.exit(1)

    if not Path(args.data_path).exists():
        print(f"Error: The path '{args.json_path}' does not exist!")
        sys.exit(1)

    if not Path(args.json_path).exists():
        print(f"Error: The path '{args.json_path}' is neither a directory nor a JSON file!")
        sys.exit(1)

    AnnotationController(Path(args.json_path), Path(args.data_path), args.video_mode)

if __name__ == '__main__':
    main()
