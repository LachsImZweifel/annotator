import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication

from src.input_handler import InputHandler
from src.annotation_cache import AnnotationCache
from src.gui.app import App

class AnnotationController:
    def __init__(self, json_path:Path, data_path:Path, video_mode:bool=False):
        self._app = QApplication([])
        self._input_handler = InputHandler(data_path, video_mode)
        self._gui = App()
        self._annotation_cache = AnnotationCache(json_path, data_path.name)

        # Signals
        self._gui.next_img.connect(self._next_image)
        self._gui.prev_img.connect(self._previous_image)
        self._gui.point_clicked.connect(self._set_keypoint)

        self._next_image()
        self._run_gui()

    def _run_gui(self):
        self._gui.show()
        sys.exit(self._app.exec())

    def _next_image(self):
        next = self._input_handler.next_image()
        if next is not None:
            name, index, image = next
            print("index " + str(index))
            self._annotation_cache.new_image(name, index, image)
            keypoints = self._annotation_cache.get_keypoints()
            print(keypoints)
            self._gui.new_image(image, keypoints)

    def _previous_image(self):
        previous = self._input_handler.previous_image()
        if previous is not None:
            name, index, image = previous
            print("index " + str(index))
            self._annotation_cache.new_image(name, index, image)
            keypoints = self._annotation_cache.get_keypoints()
            print(keypoints)
            self._gui.new_image(image, keypoints)

    def _set_keypoint(self, coordinates: tuple):
        print(f"Keypoint gesetzt bei: {coordinates}")







