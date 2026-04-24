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

    ####### GETTER SETTER ########

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

    def set_image(self, name: str, index: int, image: ImageGUI):
        self._current_image = ImageMeta(
            id=index,
            file_name=name,
            width=image.width,
            height=image.height,
            license=LICENSE["id"]
        )

    ######## LOAD / SAVE #########

    def _coco_processing(self) -> dict[int, list[dict]]:
        """ Coco -> Python convertion !!! """
        indexed_annotations = defaultdict(list)
        for annotation_coco in self._data_coco["annotations"]:
            annotation_py = annotation_to_py(Annotation(**annotation_coco))
            indexed_annotations[annotation_py.image_id].append(annotation_py.__dict__)
            self._total_annotations += 1
            self.highest_track_id = max(annotation_coco["track_id"], self.highest_track_id)

        return indexed_annotations


    def save_data(self, skeletons: list[Skeleton]):
        """ Python to coco convertion !!! """
        self._add_image()
        for skeleton in skeletons:
            self._total_annotations += 1
            self._add_skeleton(skeleton)
        with self.json_path.open("w", encoding="utf-8") as f:
            json.dump(self._data_coco, f, indent=4, ensure_ascii=False)

    def _add_image(self):
        image_coco = image_to_coco(self._current_image)
        images = self._data_coco["images"]

        for i, img in enumerate(images):
            if img["id"] == image_coco.id:
                images[i] = image_coco.__dict__
                return

        images.append(image_coco.__dict__)

    def _add_skeleton(self, skeleton: Skeleton):
        annotation_py = Annotation(
            id=self._total_annotations,
            image_id=self._current_image.id,
            category_id=skeleton.category_id,
            track_id=skeleton.track_id,
            num_keypoints=skeleton.num_keypoints,
            keypoints=skeleton.get_keypoints_flattened(),
            bbox=skeleton.bbox,
            area=skeleton.area,
            iscrowd=0
        )
        annotation_coco = annotation_to_coco(annotation_py)
        coco_annotations = self._data_coco["annotations"]

        for i, annotation in enumerate(coco_annotations):
            if annotation["image_id"] == annotation_coco.image_id \
                and annotation["track_id"] == annotation_coco.track_id:
                # save in coco data
                coco_annotations[i] = annotation_coco.__dict__
                # save in py annotations
                py_image_annotations = self._annotations[annotation_py.image_id]
                for i, annotation_py in enumerate(py_image_annotations):
                    if annotation_py["track_id"] == annotation_coco.track_id:
                        py_image_annotations[i] = annotation_py.__dict__
                return

        self._data_coco["annotations"].append(annotation_coco.__dict__)
        self._annotations[self._current_image.id].append(annotation_py.__dict__)

    @staticmethod
    def _create_json(json_path: Path, input_name: str) -> Path:
        json_path = json_path / f"{input_name.lower()}_annotations.json"
        with json_path.open(mode="w") as json_file:
            json.dump(coco, json_file, indent=4)
        return json_path








