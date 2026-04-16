import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication

from src.config import KEYPOINTS
from src.utils.types_and_dataclasses import Keypoint
from src.input_handler import InputHandler
from src.annotation_cache import AnnotationCache
from src.gui.app import App
from src.skeleton import Skeleton

class AnnotationController:
    def __init__(self, json_path:Path, data_path:Path, video_mode:bool=False):
        # Instances
        self._app = QApplication([])
        self._input_handler = InputHandler(data_path, video_mode)
        self._gui = App()
        self._annotation_cache = AnnotationCache(json_path, data_path.name)

        # Variables
        self._img_index = 0
        self._skeleton_index = 0
        self._skeletons = []

        # Signals
        self._gui.next_img.connect(self._on_next_img)
        self._gui.prev_img.connect(self._on_prev_img)
        self._gui.get_img.connect(self._on_get_img)
        self._gui.point_clicked.connect(self._on_set_kp)
        self._gui.next_kp.connect(self._on_next_kp)
        self._gui.prev_kp.connect(self._on_prev_kp)

        # Run
        self._new_image()
        self._run_gui()

    def _run_gui(self):
        self._gui.show()
        sys.exit(self._app.exec())

    def _set_index(self, index):
        self._img_index = max(0, min(index, self._input_handler.total_frames))

    def _new_image(self):
        new_img = self._input_handler.new_image(self._img_index)
        if new_img is not None:
            name, image = new_img
            self._annotation_cache.new_image(name, self._img_index, image)
            keypoints = self._annotation_cache.get_keypoints()
            self._gui.new_image(image, keypoints)
            print(self._img_index)
            print(keypoints)

    def _create_skeleton(self) -> Skeleton:
        self._skeletons.append(Skeleton(len(self._skeletons), 1, len(KEYPOINTS)))
        return self._skeletons[-1]

    ######## SIGNAL HANDLERS ########
    def _on_next_img(self):
        self._set_index(self._img_index + 1)
        self._new_image()

    def _on_prev_img(self):
        self._set_index(self._img_index - 1)
        self._new_image()

    def _on_get_img(self, index):
        self._set_index(index)
        self._new_image()

    def _on_set_kp(self, keypoint: Keypoint):
        try: self._skeletons[self._skeleton_index].set_keypoint(keypoint)
        except IndexError:
            self._create_skeleton().set_keypoint(keypoint)

    def _on_next_kp(self):
        try:
            self._skeletons[self._skeleton_index].next_keypoint()
        except IndexError:
            self._create_skeleton().next_keypoint()

    def _on_prev_kp(self):
        try:
            self._skeletons[self._skeleton_index].prev_keypoint()
        except IndexError:
            self._create_skeleton().prev_keypoint()







