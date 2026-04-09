from datetime import date

from src.config import KEYPOINTS, SKELETON

today = date.today()

coco = {
    "info": {
        "description": "Schwimmer Keypoint Annotation – Beispieldatei",
        "version": "1.0",
        "year": str(today.year),
        "contributor": "TecKnowLogic",
        "date_created": f"{today.year}-{today.month}-{today.day}"
      },

    "licenses": [
        {
          "id": 1,
          "name": "n/A",
          "url": "<n/A"
        }
    ],

    "categories": [
        {
          "id": 1,
          "name": "swimmer",
          "supercategory": "human",
          "keypoints": KEYPOINTS,
          "skeleton": SKELETON,
        }
      ],

    "images": [],

    "annotations": [],
}