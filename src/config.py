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

SKELETON: list[tuple[int, int]] = [
    (0, 1), (0, 4),         # Head to shoulders
    (1, 4),                 # Shoulder to shoulder
    (1, 2), (2, 3),         # Left arm
    (4, 5), (5, 6),         # Right arm
    (1, 7), (4, 10),        # Shoulders to hips
    (7, 10),                # Hip to hip
    (7, 8), (8, 9),         # Left leg
    (10, 11), (11, 12),     # Right leg
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