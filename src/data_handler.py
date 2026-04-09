import cv2
from collections import deque
from pathlib import Path

from src.config import SUPPORTED_FORMATS as FORMATS
from src.utils.custom_dataclasses import ImageGUI

class DataHandler:
    def __init__(self, data_path:str, video_mode:bool=False):
        self._data_path = data_path
        self._source = self._iterate_video() if video_mode else self._iterate_folder()
        self._buffer = deque()

    def _iterate_folder(self):
        for file in Path(self._data_path).iterdir():
            if file.suffix.lower() in FORMATS:
                img = cv2.imread(str(file))
                if img is not None:
                    yield cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def _iterate_video(self):
        video = cv2.VideoCapture(self._data_path)

        if not video.isOpened():
            raise ValueError(f"Error: Could not open video file '{self._data_path}'")

        try:
            while True:
                ret, frame = video.read()
                if not ret:
                    break
                yield cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        finally:
            video.release()

    def next_image(self):
        try:
            image_rgb = next(self._source)
        except StopIteration:
            return None
        self._buffer.append(image_rgb)
        return self._to_image_data(image_rgb)

    def previous_image(self, steps=1):
        if steps >= len(self._buffer):
            return None
        self._buffer.pop()
        return self._to_image_data(self._buffer[- steps])

    @staticmethod
    def _to_image_data(image_rgb):
        height, width, channels = image_rgb.shape
        bytes_per_line = channels * width

        return ImageGUI(image_rgb.tobytes(), width, height, bytes_per_line, channels)