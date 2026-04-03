import argparse
import os
import sys
from src.AnnotationController import AnnotationController

def main():
    parser = argparse.ArgumentParser(description='Annotator - A tool for annotating human pose datasets.')
    parser.add_argument('data_path', type=str, help='Path to the data to be annotated.')
    parser.add_argument('--video_mode', action='store_true', help='Enable video mode for annotation.')

    args = parser.parse_args()

    if not os.path.exists(args.data_path):
        print(f"Fehler: Der Pfad '{args.data_path}' existiert nicht!")
        sys.exit(1)

    AnnotationController(args.data_path, args.video_mode)

if __name__ == '__main__':
    main()
