from typing import Generator

import cv2
from collections import deque
from pathlib import Path

from numpy import ndarray

from src.config import SUPPORTED_FORMATS as FORMATS
from src.utils.types_and_dataclasses import ImageGUI

class InputHandler:
    def __init__(self, data_path: Path, video_mode: bool=False):
        self._data_path = data_path
        self._source = self._iterate_video() if video_mode else self._iterate_folder()
        self._buffer: deque[tuple[str, int, ndarray]] = deque()

    def _iterate_folder(self) -> Generator[tuple[str, int, ndarray]]:
        for i, file in enumerate(Path(self._data_path).iterdir()):
            if file.suffix.lower() in FORMATS:
                img = cv2.imread(str(file))
                if img is not None:
                    yield str(file), i, cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def _iterate_video(self) -> Generator[tuple[str, int, ndarray]]:
        video = cv2.VideoCapture(self._data_path)

        if not video.isOpened():
            raise ValueError(f"Error: Could not open video file '{self._data_path}'")

        try:
            i = 0
            while True:
                ret, frame = video.read()
                if not ret:
                    break
                yield self._data_path.name, i, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        finally:
            video.release()

    def next_image(self) -> tuple[str, int, ImageGUI] | None:
        try:
            name, index, image_rgb = next(self._source)
        except StopIteration:
            return None
        self._buffer.append((name, index, image_rgb))
        return name, index, self._to_image_data(image_rgb)

    def previous_image(self, steps: int = 1) -> tuple[str, int, ImageGUI] | None:
        if steps >= len(self._buffer):
            return None
        self._buffer.pop()
        name, index, image_rgb = self._buffer[-steps]
        return name, index, self._to_image_data(image_rgb)

    @staticmethod
    def _to_image_data(image_rgb: ndarray) -> ImageGUI:
        height, width, channels = image_rgb.shape
        bytes_per_line = channels * width

        return ImageGUI(image_rgb.tobytes(), width, height, bytes_per_line, channels)