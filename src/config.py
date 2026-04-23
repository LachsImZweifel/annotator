import pathlib
from typing import Any

BASE_DIR = pathlib.Path(__file__).parent.parent.resolve()

#Annotation Constants
LICENSE: dict[str, Any] = {
      "id": 1,
      "name": "TecKnowLogic",
      "url": "TecKnowLogic.com"
    }

KEYPOINTS: list[str] = [
    "head", "left_shoulder", "left_elbow", "left_hand",
    "right_shoulder", "right_elbow", "right_hand",
    "left_hip", "left_knee", "left_foot",
    "right_hip", "right_knee", "right_foot"
]

SKELETON_COCO: list[tuple[int, int]] = [
    (1, 2), (1, 5),         # Head to shoulders
    (2, 5),                 # Shoulder to shoulder
    (2, 3), (3, 4),         # Left arm
    (5, 6), (6, 7),         # Right arm
    (2, 8), (5, 11),        # Shoulders to hips
    (8, 11),                # Hip to hip
    (8, 9), (9, 10),        # Left leg
    (11, 12), (12, 13),     # Right leg
]

# GUI Constants
KEYPOINT_SIZE: int = 6
KEYPOINT_COLORS: dict[str, list[int]] = {
    "#a855f7": [0],         # purple, head
    "#22c55e": [1,2,3],     # bright green, left arm
    "#ef4444": [4,5,6],     # bright red, right arm
    "#15803d": [7,8,9],     # dark green, left leg
    "#991b1b": [10,11,12],  # dark red, right leg

}

# Input Constants
SUPPORTED_FORMATS: set[str] = {
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