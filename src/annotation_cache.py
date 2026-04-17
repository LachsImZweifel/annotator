import json
from pathlib import Path
from collections import defaultdict

from src.config import LICENSE
from src.skeleton import Skeleton
from src.utils.coco_starter import coco
from src.utils.types_and_dataclasses import ImageGUI, ImageCOCO, SkeletonsData, AnnotationCOCO


class AnnotationCache:
    def __init__(self, json_path: Path, input_name: str):
        self.json_path, self._data = self._setup(json_path, input_name)
        self._total_annotations = 0
        self._annotations = self._annotation_indexing()
        self._current_image = None

    def _setup(self, json_path: Path, input_name: str) -> json:
        if json_path.is_dir():
            json_path = self._create_json(json_path, input_name)
        elif json_path.stat().st_size == 0:
            with json_path.open(mode="w") as json_file:
                json.dump(coco, json_file, indent=4)
        with json_path.open(mode="r") as json_file:
            return json_path, json.load(json_file)

    def _annotation_indexing(self) -> dict[int, list[dict]]:
        indexed_annotations = defaultdict(list)
        for annotation in self._data["annotations"]:
            self._total_annotations += 1
            indexed_annotations[annotation["image_id"]].append(annotation)
        return indexed_annotations

    def set_image(self, name: str, index: int, image: ImageGUI):
        self._current_image = ImageCOCO(
            id=index + 1,
            file_name=name,
            width=image.width,
            height=image.height,
            license=LICENSE["id"]
        )

    def save_image_data(self, skeletons: list[Skeleton]):
        self._data["images"].append(self._current_image.__dict__)
        for skeleton in skeletons:
            self._total_annotations += 1
            annotation = AnnotationCOCO(
                id = self._total_annotations,
                image_id = self._current_image.id,
                category_id = skeleton.category_id,
                num_keypoints = skeleton.num_keypoints,
                keypoints = skeleton.get_keypoints_flattened(),
                bbox = skeleton.bbox,
                area = skeleton.area,
                iscrowd = 0
            )
            self._data["annotations"].append(annotation.__dict__)
            self._annotations[self._current_image.id].append(annotation.__dict__)

        with self.json_path.open("w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=4, ensure_ascii=False)


    def get_keypoints(self, image_index) -> SkeletonsData:
        image_annotations = self._annotations.get(image_index, None)
        if image_annotations is None: return []

        image_keypoints: SkeletonsData = []
        for annotation in image_annotations:
            ungrouped = annotation["keypoints"]
            if len(ungrouped) % 3 != 0:
                raise ValueError("Wrong keypoints format, must be (x,y,visibility)")
            grouped: list[tuple[int, int, int]] = [
                (ungrouped[i], ungrouped[i + 1], ungrouped[i + 2])
                for i in range(0, len(ungrouped), 3)
            ]
            image_keypoints.append(grouped)
        return image_keypoints

    @staticmethod
    def _create_json(json_path: Path, input_name: str) -> Path:
        json_path = json_path / f"{input_name.lower()}_annotations.json"
        with json_path.open(mode="w") as json_file:
            json.dump(coco, json_file, indent=4)
        return json_path








