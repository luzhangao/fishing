# coding:utf8

"""
@author: Zhangao Lu
@contact: zlu2@laurentian.ca
@time: 2022/4/7
@description:
"""

import os
import torch

# Model
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model = torch.hub.load(r'yolov5', 'custom', path=r'models\best.pt', source='local')


# Images
# img = 'https://ultralytics.com/images/zidane.jpg'  # or file, Path, PIL, OpenCV, numpy, list
file_path = r"datasets\fishing_roboflow\train\images"
file_path = r"raw_data"

for img in os.listdir(file_path):

    # img = r'datasets\fishing_roboflow\train\images\WoWScrnShot_033022_114407_jpg.rf.8ab784666c6115a4c62942fba1ed1bb1.jpg'  # or file, Path, PIL, OpenCV, numpy, list

    # Inference 640
    results = model(file_path + r"\\" + img)

    # Results
    results.print()
    results.show()


if __name__ == '__main__':
    pass
