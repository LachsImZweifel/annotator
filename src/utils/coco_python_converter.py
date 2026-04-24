from tkinter import Image

from src.utils.types_and_dataclasses import Annotation, ImageMeta


def annotation_to_py(annotation: Annotation) -> Annotation:
    annotation_py = Annotation(
        id=annotation.id,
        image_id=annotation.image_id - 1,
        category_id=annotation.category_id,
        track_id=annotation.track_id - 1,
        num_keypoints=annotation.num_keypoints,
        keypoints=annotation.keypoints,
        bbox=annotation.bbox,
        area=annotation.area,
        iscrowd=annotation.iscrowd,
    )
    return annotation_py

def annotation_to_coco(annotation: Annotation) -> Annotation:
    annotation_coco = Annotation(
        id=annotation.id,
        image_id=annotation.image_id + 1,
        category_id=annotation.category_id,
        track_id=annotation.track_id + 1,
        num_keypoints=annotation.num_keypoints,
        keypoints=annotation.keypoints,
        bbox=annotation.bbox,
        area=annotation.area,
        iscrowd=annotation.iscrowd
    )
    return annotation_coco

def image_to_coco(image: ImageMeta) -> ImageMeta:
    image_coco = image
    image_coco.id += 1
    return image_coco

def image_to_py(image: ImageMeta) -> ImageMeta:
    image_py = image
    image_py.id += 1
    return image_py