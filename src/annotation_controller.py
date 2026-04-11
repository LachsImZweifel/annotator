import sys
from pathlib import Path
from typing import Literal, Optional
from PyQt6.QtWidgets import QApplication

from src.input_handler import InputHandler
from src.annotation_cache import AnnotationCache
from src.gui.app import App

class AnnotationController:
    def __init__(self, json_path:Path, data_path:Path, video_mode:bool=False):
        # Instances
        self._app = QApplication([])
        self._input_handler = InputHandler(data_path, video_mode)
        self._gui = App()
        self._annotation_cache = AnnotationCache(json_path, data_path.name)

        # Variables
        self._index = 0

        # Signals
        self._gui.next_img.connect(self._on_next)
        self._gui.prev_img.connect(self._on_prev)
        self._gui.get_img.connect(self._on_get)
        self._gui.point_clicked.connect(self._set_keypoint)

        # Run
        self._new_image()
        self._run_gui()

    def _run_gui(self):
        self._gui.show()
        sys.exit(self._app.exec())

    def _on_next(self):
        self._index += 1
        self._new_image()

    def _on_prev(self):
        self._index -= 1
        self._new_image()

    def _on_get(self, index):
        self._index = index
        self._new_image()

    def _new_image(self):
        new_img = self._input_handler.new_image(self._index)
        if new_img is not None:
            name, image = new_img
            self._annotation_cache.new_image(name, self._index, image)
            keypoints = self._annotation_cache.get_keypoints()
            self._gui.new_image(image, keypoints)
            print(self._index)
            print(keypoints)

    def _set_keypoint(self, coordinates: tuple):
        print(f"Keypoint gesetzt bei: {coordinates}")







