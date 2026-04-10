from datetime import date
from typing import Dict, Any

from src.config import KEYPOINTS, SKELETON, LICENSE

today = date.today()

coco: Dict[str, Any] = {
    "info": {
        "description": "Schwimmer Keypoint Annotation – Beispieldatei",
        "version": "1.0",
        "year": str(today.year),
        "contributor": "TecKnowLogic",
        "date_created": f"{today.year}-{today.month}-{today.day}"
      },

    "licenses": [LICENSE],

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