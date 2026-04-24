import json
from pathlib import Path
from collections import defaultdict

from src.config import LICENSE
from src.skeleton import Skeleton
from src.utils.coco_starter import coco
from src.utils.types_and_dataclasses import ImageGUI, ImageMeta, Annotation, Keypoint
from src.utils.coco_python_converter import annotation_to_py, annotation_to_coco, image_to_coco, image_to_py


class AnnotationCache:
    def __init__(self, json_path: Path, input_name: str):
        self.json_path, self._data_coco = self._setup(json_path, input_name)
        self._total_annotations = 0
        self.highest_track_id = 0
        self._annotations = self._coco_processing()
        self._current_image = None

    def _setup(self, json_path: Path, input_name: str) -> json:
        if json_path.is_dir():
            json_path = self._create_json(json_path, input_name)
        elif json_path.stat().st_size == 0:
            with json_path.open(mode="w") as json_file:
                json.dump(coco, json_file, indent=4)
        with json_path.open(mode="r") as json_file:
            return json_path, json.load(json_file)

    def _coco_processing(self) -> dict[int, list[dict]]:
        """ Coco -> Python convertion !!! """
        indexed_annotations = defaultdict(list)
        for annotation_coco in self._data_coco["annotations"]:
            annotation_py = annotation_to_py(annotation_coco)
            indexed_annotations[annotation_py.track_id].append(annotation_py)
            self._total_annotations += 1
            self.highest_track_id = max(annotation_coco["track_id"], self.highest_track_id)

        return indexed_annotations

    def set_image(self, name: str, index: int, image: ImageGUI):
        self._current_image = ImageMeta(
            id=index,
            file_name=name,
            width=image.width,
            height=image.height,
            license=LICENSE["id"]
        )

    def save_image_data(self, skeletons: list[Skeleton]):
        """ Python to coco convertion !!! """
        image_coco = image_to_coco(self._current_image)
        self._data_coco["images"].append(image_coco.__dict__)
        for skeleton in skeletons:
            self._total_annotations += 1
            annotation_py = Annotation(
                id = self._total_annotations,
                image_id = self._current_image.id,
                category_id = skeleton.category_id,
                track_id = skeleton.track_id,
                num_keypoints = skeleton.num_keypoints,
                keypoints = skeleton.get_keypoints_flattened(),
                bbox = skeleton.bbox,
                area = skeleton.area,
                iscrowd = 0
            )
            annotation_coco = annotation_to_coco(annotation_py)
            self._data_coco["annotations"].append(annotation_coco.__dict__)
            self._annotations[self._current_image.id].append(annotation_py.__dict__)

        with self.json_path.open("w", encoding="utf-8") as f:
            json.dump(self._data_coco, f, indent=4, ensure_ascii=False)

    def get_annotations(self, image_index) -> dict[int, list[Keypoint]]:
        image_annotations = self._annotations.get(image_index, None)
        if image_annotations is None: return {}

        skeleton_keypoints_dict: dict[int, list[Keypoint]] = defaultdict(list)
        for annotation in image_annotations:
            track_id = annotation["track_id"]
            ungrouped = annotation["keypoints"]
            if len(ungrouped) % 3 != 0:
                raise ValueError("Wrong keypoints format, must be (x,y,visibility)")
            grouped: list[tuple[int, int, int]] = [
                (ungrouped[i], ungrouped[i + 1], ungrouped[i + 2])
                for i in range(0, len(ungrouped), 3)
            ]
            skeleton_keypoints_dict[track_id] = grouped
        return skeleton_keypoints_dict

    @staticmethod
    def _create_json(json_path: Path, input_name: str) -> Path:
        json_path = json_path / f"{input_name.lower()}_annotations.json"
        with json_path.open(mode="w") as json_file:
            json.dump(coco, json_file, indent=4)
        return json_path








