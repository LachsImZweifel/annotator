from typing import Tuple, List, Literal
from dataclasses import dataclass

SkeletonCOCO = List[Tuple[int, int, int]]
KeypointsCOCO = List[SkeletonCOCO]

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
class Annotation:
    id: int
    image_id: int
    category_id: int
    num_keypoints: int
    keypoints: List[Tuple[int, int, int]]
    bbox: Tuple[int, int, int, int]
    area: int
    iscrowd: 0 | 1



