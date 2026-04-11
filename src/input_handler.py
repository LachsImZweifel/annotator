import cv2
from collections import deque
from pathlib import Path

from numpy import ndarray

from src.config import SUPPORTED_FORMATS as FORMATS
from src.utils.types_and_dataclasses import ImageGUI


class InputHandler:
    def __init__(self, data_path: Path, video_mode: bool=False):
        self._source = VideoSource(data_path) if video_mode else FolderSource(data_path)
        self._total_frames = self._source.total_frames

    @property
    def total_frames(self) -> int:
        return self._total_frames

    def new_image(self, index) -> tuple[str, ImageGUI] | None:
        name, frame = self._source.get_frame(index)
        if frame is None: return None
        return name, self._to_image_data(frame)

    @staticmethod
    def _to_image_data(image_rgb: ndarray) -> ImageGUI:
        height, width, channels = image_rgb.shape
        bytes_per_line = channels * width

        return ImageGUI(image_rgb.tobytes(), width, height, bytes_per_line, channels)


class VideoSource:
    def __init__(self, path: Path):
        self._filename = path.name
        self._video = cv2.VideoCapture(str(path))
        self._total_frames = int(self._video.get(cv2.CAP_PROP_FRAME_COUNT))
        self._cache = {}
        self._cache_order = deque()

    @property
    def total_frames(self) -> int:
        return self._total_frames

    def get_frame(self, index: int) -> tuple[str, ndarray]:
        if index in self._cache:
            return self._cache[index]

        self._video.set(cv2.CAP_PROP_POS_FRAMES, index)
        ret, frame = self._video.read()
        if not ret:
            raise ValueError(f"Could not read frame {index}")

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self._store(index, rgb)
        return self._filename, rgb

    def _store(self, index: int, frame: ndarray):
        if len(self._cache) >= 20:
            oldest = self._cache_order.popleft()
            del self._cache[oldest]
        self._cache[index] = frame
        self._cache_order.append(index)

    def close(self):
        self._video.release()


class FolderSource:
    def __init__(self, path: Path):
        self._paths = sorted([
            p for p in path.iterdir()
            if p.suffix.lower() in FORMATS
        ])

    @property
    def total_frames(self) -> int:
        return len(self._paths)

    def get_frame(self, index: int) -> tuple[str, ndarray]:
        name = self._paths[index].name
        img = cv2.imread(str(self._paths[index]))
        return name, cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def get_name(self, index: int) -> str:
        return self._paths[index].name

