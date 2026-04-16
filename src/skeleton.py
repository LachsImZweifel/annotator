from typing import Optional
from src.utils.types_and_dataclasses import Keypoint

class Skeleton:
    def __init__(self, track_id: int, category_id: int, num_keypoints: int):
        self.track_id = track_id
        self.category_id = category_id
        self.num_keypoints = num_keypoints
        self.keypoint_index = 0
        self.keypoints: list[Optional[Keypoint]] = num_keypoints * [None]

    def set_keypoint(self, keypoint: Keypoint):
        self.keypoints[self.keypoint_index] = keypoint
        self.keypoint_index = (self.keypoint_index + 1) % self.num_keypoints
        print("Keypoint saved: ", self.keypoints[self.keypoint_index - 1])


    def next_keypoint(self):
        if self.keypoints[self.keypoint_index] is None:
            self.keypoints[self.keypoint_index] = (0, 0, 0)
        self.keypoint_index = (self.keypoint_index + 1) % self.num_keypoints
        print("Keypoint saved: ", self.keypoints[self.keypoint_index - 1])

    def prev_keypoint(self):
        if self.keypoints[self.keypoint_index] is None:
            self.keypoints[self.keypoint_index] = (0, 0, 0)
        self.keypoint_index = (self.keypoint_index - 1) % self.num_keypoints
        print("Prev Keypoint: ", self.keypoints[self.keypoint_index])
