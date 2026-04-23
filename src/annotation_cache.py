import json
from pathlib import Path
from collections import defaultdict

from src.config import LICENSE
from src.skeleton import Skeleton
from src.utils.coco_starter import coco
from src.utils.types_and_dataclasses import ImageGUI, ImageCOCO, SkeletonsData, AnnotationCOCO, Keypoint


class AnnotationCache:
    def __init__(self, json_path: Path, input_name: str):
        self.json_path, self._data = self._setup(json_path, input_name)
        self._total_annotations = 0
        self._annotations = self._annotation_indexing()
        self._coco_image = None

    def _setup(self, json_path: Path, input_name: str) -> json:
        if json_path.is_dir():
            json_path = self._create_json(json_path, input_name)
        elif json_path.stat().st_size == 0:
            with json_path.open(mode="w") as json_file:
                json.dump(coco, json_file, indent=4)
        with json_path.open(mode="r") as json_file:
            return json_path, json.load(json_file)

    def _annotation_indexing(self) -> dict[int, list[dict]]:
        """ Coco -> Python convertion: SUBSTRACT 1 to ID's and skeleton connections !!! """
        indexed_annotations = defaultdict(list)
        for annotation in self._data["annotations"]:
            self._total_annotations += 1
            py_index = int(annotation["image_id"] - 1)
            indexed_annotations[py_index].append(annotation)
        return indexed_annotations

    def set_image(self, name: str, index: int, image: ImageGUI):
        """ Python to coco convertion: ADD 1  to ID's and skeleton connections !!! """
        self._coco_image = ImageCOCO(
            id=index + 1,
            file_name=name,
            width=image.width,
            height=image.height,
            license=LICENSE["id"]
        )

    def save_image_data(self, py_index: int, skeletons: list[Skeleton]):
        """ Python to coco convertion: ADD 1  to ID's and skeleton connections !!! """
        self._data["images"].append(self._coco_image.__dict__)
        for skeleton in skeletons:
            self._total_annotations += 1
            annotation = AnnotationCOCO(
                id = self._total_annotations,
                image_id = self._coco_image.id, #Already +1
                category_id = skeleton.category_id,
                track_id = skeleton.track_id + 1,
                num_keypoints = skeleton.num_keypoints,
                keypoints = skeleton.get_keypoints_flattened(),
                bbox = skeleton.bbox,
                area = skeleton.area,
                iscrowd = 0
            )
            self._data["annotations"].append(annotation.__dict__)
            self._annotations[py_index].append(annotation.__dict__)

        with self.json_path.open("w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=4, ensure_ascii=False)

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








