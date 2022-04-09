# coding:utf8

"""
@author: Zhangao Lu
@contact: zlu2@laurentian.ca
@time: 2022/4/8
@description:
"""

import io
import os
import cv2
import requests
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder
from dectector.utils.display_images import visualize, roboflow_to_coco
from dectector.utils.settings import api_key


# file_path = r"datasets\fishing_roboflow\train\images"
file_path = r"raw_data"
image_width = 640
image_height = 640
category_id_to_name = {0: "fish-float", 1: "fish-float-catched"}
category_name_to_id = {v: k for k, v in category_id_to_name.items()}

for img in os.listdir(file_path):
    # Load Image with PIL
    img = cv2.imread(file_path + r"\\" + img)
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pilImage = Image.fromarray(image)

    # Convert to JPEG Buffer
    buffered = io.BytesIO()
    pilImage.save(buffered, quality=100, format="JPEG")

    # Build multipart form and post request
    m = MultipartEncoder(fields={'file': ("imageToUpload", buffered.getvalue(), "image/jpeg")})
    response = requests.post(f"https://detect.roboflow.com/fishing-ammt4/1?api_key={api_key}", data=m, headers={'Content-Type': m.content_type})

    print(response)
    print(response.json())
    predictions = response.json()["predictions"]
    bbox_lists = list()
    category_ids = list()
    confidences = list()
    for pred in predictions:
        # {'x': 304.0, 'y': 105.5, 'width': 16, 'height': 23, 'class': 'fish-float', 'confidence': 0.575}
        roboflow_bbox = [pred["x"], pred["y"], pred["width"], pred["height"]]
        coco_bbox = roboflow_to_coco(roboflow_bbox)
        bbox_lists.append(coco_bbox)
        category_ids.append(category_name_to_id[pred["class"]])
        confidences.append(pred["confidence"])
    visualize(img, bbox_lists, category_ids, category_id_to_name, confidences)


if __name__ == '__main__':
    pass
