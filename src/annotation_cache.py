import json
from pathlib import Path
from collections import defaultdict

from src.config import LICENSE
from src.utils.coco_starter import coco
from src.utils.types_and_dataclasses import ImageGUI, ImageCOCO, Annotation, KeypointsCOCO


class AnnotationCache:
    def __init__(self, json_path: Path, input_name: str):
        # read
        self._data = self._setup(json_path, input_name)
        self._annotations = self._annotation_indexing()
        # write
        self._current_image = None
        self._new_annotations: list[Annotation] = []

    def _setup(self, json_path: Path, input_name: str) -> json:
        if json_path.is_dir():
            json_path = self._create_json(json_path, input_name)
        elif json_path.stat().st_size == 0:
            with json_path.open(mode="w") as json_file:
                json.dump(coco, json_file, indent=4)
        with json_path.open(mode="r") as json_file:
            return json.load(json_file)

    def _annotation_indexing(self) -> dict[int, list[dict]]:
        indexed_annotations = defaultdict(list)
        for annotation in self._data["annotations"]:
            indexed_annotations[annotation["image_id"]].append(annotation)
        return indexed_annotations

    def new_image(self, name: str, index: int, image: ImageGUI):
        #save data
        self._current_image = ImageCOCO(
            id=index,
            file_name=name,
            width=image.width,
            height=image.height,
            license=LICENSE["id"]
        )
        #load data

    def get_keypoints(self) -> KeypointsCOCO:
        image_annotations = self._annotations.get(self._current_image.id, None)
        if image_annotations is None: return []

        image_keypoints: KeypointsCOCO = []
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








