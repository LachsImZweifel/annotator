from typing import Tuple, List, Literal
from dataclasses import dataclass

Keypoint = Tuple[int, int, int]
SkeletonsData = List[List[Keypoint]]
Shapes = Literal["triangle_up", "triangle_down", "x", "text"]

@dataclass
class ImageGUI:
    data: bytes
    width: int
    height: int
    bytes_per_line: int
    channels: int

@dataclass
class ImageCOCO:
    id: int
    file_name: str
    width: int
    height: int
    license: int

@dataclass
class AnnotationCOCO:
    id: int
    image_id: int
    category_id: int
    track_id: int
    num_keypoints: int
    keypoints: List[int]
    bbox: Tuple[int, int, int, int]
    area: float
    iscrowd: 0 | 1



