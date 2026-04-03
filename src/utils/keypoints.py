from dataclasses import make_dataclass
from typing import Optional, Tuple
from src.config import KEYPOINTS

PersonKeypoints = make_dataclass(
    "Keypoints",
    [(name, Optional[Tuple[int, int]], None) for name in KEYPOINTS]
)