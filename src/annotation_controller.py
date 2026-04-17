import sys
from typing import Optional
from pathlib import Path
from PyQt6.QtWidgets import QApplication

from src.config import KEYPOINTS
from src.utils.types_and_dataclasses import Keypoint, SkeletonsData
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

        # States & Variables
        self._img_index = 0
        self._skeleton_index = 0
        self._skeletons = []

        # Signals
        self._gui.next_img.connect(self._on_next_img)
        self._gui.prev_img.connect(self._on_prev_img)
        self._gui.get_img.connect(self._on_get_img)
        self._gui.set_kp.connect(self._on_set_kp)
        self._gui.next_kp.connect(self._on_next_kp)
        self._gui.prev_kp.connect(self._on_prev_kp)
        self._gui.remove_kp.connect(self._on_remove_kp)

        self._gui.skeleton_index.connect(self._on_skeleton_index)

        # Run
        self._handle_next_image()
        self._run_gui()

    def _run_gui(self):
        self._gui.show()
        sys.exit(self._app.exec())

    def _set_index(self, index):
        self._img_index = max(0, min(index, self._input_handler.total_frames))

    def _create_skeletons(self, index = None, keypoints: Optional[SkeletonsData] = None):
        if keypoints is None:
            skeleton_index = index or self._skeleton_index
            self._skeletons = [Skeleton(skeleton_index, self._img_index, 1, len(KEYPOINTS))]
            self._skeleton_index = len(self._skeletons) - 1
        else:
            self._skeletons = []
            for skeleton_data in keypoints:
                skeleton =Skeleton(self._skeleton_index, self._img_index, 1, len(KEYPOINTS))
                skeleton.load_keypoints(skeleton_data)
                self._skeletons.append(skeleton)
                self._skeleton_index = len(self._skeletons) - 1

    ########### HANDLE NEXT IMAGE ##############

    def _handle_next_image(self):
        if self._img_index > 0: self._annotation_cache.save_image_data(self._skeletons)
        self._set_new_image()
        self._update_image_data()
        self._display_image_data()

    def _set_new_image(self):
        new_img = self._input_handler.new_image(self._img_index)
        if new_img is not None:
            name, image = new_img
            self._annotation_cache.set_image(name, self._img_index, image)
            self._gui.new_image(image)

    def _display_image_data(self):
        keypoints: SkeletonsData = [skeleton.get_keypoints() for skeleton in self._skeletons]
        self._gui.new_data(keypoints)

    def _update_image_data(self):
        annotations = self._annotation_cache.get_keypoints(self._img_index)
        self._create_skeletons(annotations)

    ######## SIGNAL HANDLERS ########
    def _on_next_img(self):
        self._set_index(self._img_index + 1)
        self._handle_next_image()

    def _on_prev_img(self):
        self._set_index(self._img_index - 1)
        self._handle_next_image()

    def _on_get_img(self, index):
        self._set_index(index)
        self._handle_next_image()

    def _on_set_kp(self, keypoint: Keypoint):
        print(self._skeleton_index)
        self._skeletons[self._skeleton_index].set_keypoint(keypoint)

    def _on_next_kp(self):
        self._skeletons[self._skeleton_index].next_keypoint()

    def _on_prev_kp(self):
        self._skeletons[self._skeleton_index].prev_keypoint()

    def _on_remove_kp(self):
        self._skeletons[self._skeleton_index].remove_keypoint()

    def _on_skeleton_index(self, index):
        self._skeletons[self._skeleton_index].finish()

        if index > self._skeleton_index + 1:
            print("Index out of range")
            pass
        elif index == self._skeleton_index + 1:
            print("Creating new skeleton")
            self._skeleton_index = index
            self._create_skeletons()
        else:
            print("Switching to existing skeleton")
            self._skeleton_index = index






