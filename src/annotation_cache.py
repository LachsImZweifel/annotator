from typing import List
import json
from pathlib import Path

from src.utils.custom_dataclasses import skeleton
from src.config import KEYPOINTS


class AnnotationCache:
    def __init__(self, json_path: Path, data_path: Path):
        self.skeletons: List[skeleton] = []
        self.json_path = json_path
        self.datapath = data_path
        self.setup()

    def setup(self):
        if self.json_path.is_dir():
            self.create_json()
        if self.json_path.stat().st_size == 0:
            self.setup_coco()

    def create_json(self):
        input_name = self.datapath.name
        self.json_path = self.json_path / f"{input_name}_annotations.json"
        with self.json_path.open(mode="w") as json_file:
            json.dump({}, json_file, indent=4)

    def setup_coco(self):






        coco_format = {
            "info": {
                "description": "Annotation Cache",
                "version": "1.0",
                "year": 2024
            },
            "licenses": [],
            "categories": [
                {
                    "id": 1,
                    "name": "person",
                    "keypoints": KEYPOINTS,
                    "skeleton": skeleton
                }
            ],
            "images": [],
            "annotations": []
        }

        for idx, skeleton in enumerate(self.skeletons):
            coco_format["images"].append({
                "id": idx,
                "file_name": f"image_{idx}.jpg",
                "width": 640,  # Beispielwert, anpassen je nach Bildgröße
                "height": 480  # Beispielwert, anpassen je nach Bildgröße
            })
            coco_format["annotations"].append({
                "id": idx,
                "image_id": idx,
                "category_id": 1,
                "keypoints": skeleton.keypoints,  # Hier sollten die Keypoints im COCO-Format gespeichert werden
                "num_keypoints": len(skeleton.keypoints) // 3  # Anzahl der Keypoints (x, y, visibility)
            })

        with open(self.json_path, 'w') as json_file:
            json.dump(coco_format, json_file, indent=4)


    def load_data(self):
        return None



