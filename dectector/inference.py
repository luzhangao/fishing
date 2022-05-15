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
# file_path = r"datasets\fishing_roboflow\train\images"
file_path = r"raw_data"

for img in os.listdir(file_path):
    if img != "WoWScrnShot_033122_183244.jpg":
        # Inference
        results = model(file_path + r"\\" + img)

        for pred in results.pred:
            print(pred.cpu().numpy()[:, :4])
            print(pred.cpu().numpy()[:, 4:])

        # Results
        # print(dir(results))
        # for attr in dir(results):
        #     print(f"{attr}", eval(f"results.{attr}"))

        # results.print()
        results.show()
        # break


if __name__ == '__main__':
    pass
