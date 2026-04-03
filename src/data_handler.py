import cv2
from pathlib import Path

from src.config import SUPPORTED_FORMATS as FORMATS
from src.utils.image_data import ImageData

class DataHandler:
    def __init__(self, data_path:str, video_mode:bool=False):
        self.data_path = data_path
        self.source = self.iterate_video() if video_mode else self.iterate_folder()

    #TODO: Change to list for previous frame support
    def iterate_folder(self):
        for file in Path(self.data_path).iterdir():
            if file.suffix.lower() in FORMATS:
                img = cv2.imread(str(file))
                if img is not None:
                    yield cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def iterate_video(self):
        video = cv2.VideoCapture(self.data_path)

        if not video.isOpened():
            raise ValueError(f"Error: Could not open video file '{self.data_path}'")

        try:
            while True:
                ret, frame = video.read()
                if not ret:
                    break
                yield cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        finally:
            video.release()


    def get_image(self):
        try:
            image_rgb = next(self.source)
        except StopIteration:
            return None

        height, width, channels = image_rgb.shape
        bytes_per_line = channels * width

        return ImageData(image_rgb.tobytes(), width, height, bytes_per_line, channels)