from typing import Optional
from src.utils.types_and_dataclasses import Keypoint

class Skeleton:
    def __init__(self, track_id: int, image_id: int, category_id: int, num_keypoints: int):

        self.track_id = track_id
        self.image_id = image_id
        self.category_id = category_id
        self.num_keypoints = num_keypoints
        self.keypoint_index = 0
        self.keypoints: list[Optional[Keypoint]] = num_keypoints * [None]

    @property
    def bbox(self) -> tuple[int, int, int, int]:
        return self.calc_bbox()

    @property
    def area(self) -> float:
        bbox = self.calc_bbox()
        return bbox[2] * bbox[3]

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

    def remove_keypoint(self):
        self.keypoints[self.keypoint_index] = None
        print("Keypoint removed: ", self.keypoints[self.keypoint_index])

    def load_keypoints(self, keypoints: list[Keypoint]):
        if len(keypoints) != self.num_keypoints:
            raise ValueError("Number of keypoints does not match skeleton configuration")
        self.keypoints = keypoints

    def get_keypoints(self) -> list[Keypoint]:
        return [
            (0, 0, 0) if kp is None else kp
            for kp in self.keypoints
        ]

    def get_keypoints_flattened(self) -> list[int]:
        flattened = []
        for kp in self.keypoints:
            if kp is None:
                flattened.extend([0, 0, 0])
            else:
                flattened.extend(kp)
        return flattened

    def finish(self):
        self.keypoints = [
            (0, 0, 0) if kp is None else kp
            for kp in self.keypoints
        ]

    def clear_keypoints(self):
        self.keypoints = [None] * self.num_keypoints

    def calc_bbox(self) -> tuple[int, int, int, int]:
        x_coords = [kp[0] for kp in self.keypoints if kp is not None and kp[2] > 0]
        y_coords = [kp[1] for kp in self.keypoints if kp is not None and kp[2] > 0]
        if not x_coords or not y_coords:
            return 0, 0, 0, 0
        x_min = min(x_coords)
        y_min = min(y_coords)
        width = max(x_coords) - x_min
        height = max(y_coords) - y_min
        return x_min, y_min, width, height

    def is_empty(self) -> bool:
        return all(kp is None or kp[2] == 0 for kp in self.keypoints)

