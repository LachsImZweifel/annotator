import pathlib
from collections import OrderedDict
from typing import Tuple

BASE_DIR = pathlib.Path(__file__).parent.parent.resolve()

#Annotation Constants
KEYPOINTS= [
    "head", "left_shoulder", "left_elbow", "left_hand",
    "right_shoulder", "right_elbow", "right_hand",
    "left_hip", "left_knee", "left_foot",
    "right_hip", "right_knee", "right_foot"
]

#Library Constants
SUPPORTED_FORMATS = {
        '.jpg', '.jpeg', '.jpe',        # JPEG Formate
        '.png',                         # Portable Network Graphics
        '.bmp', '.dib',                 # Windows Bitmaps
        '.webp',                        # Google WebP
        '.tiff', '.tif',                # TIFF Formate
        '.jp2',                         # JPEG 2000
        '.pbm', '.pgm', '.ppm', '.pxm', # Portable Messwerte
        '.sr', '.ras',                  # Sun Rasters
        '.hdr', '.pic'                  # HDR Formate
}