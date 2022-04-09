# coding:utf8

"""
@author: Zhangao Lu
@contact: zlu2@laurentian.ca
@time: 2021/10/10
@description:
Display the picture with bounding box
"""


import cv2
import pandas as pd
from matplotlib import pyplot as plt


BOX_COLOR = (255, 0, 0)  # Red
TEXT_COLOR = (255, 255, 255)  # White


def visualize_bbox(img, bbox, class_name, class_confidence, color=BOX_COLOR, thickness=2):
    """Visualizes a single bounding box on the image"""
    x_min, y_min, w, h = bbox
    x_min, x_max, y_min, y_max = int(x_min), int(x_min + w), int(y_min), int(y_min + h)

    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color=color, thickness=thickness)

    ((text_width, text_height), _) = cv2.getTextSize(class_name, cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1)
    cv2.rectangle(img, (x_min, y_min - int(1.3 * text_height)), (x_min + text_width, y_min), BOX_COLOR, -1)
    cv2.putText(
        img,
        text=f"{class_name} {class_confidence}",
        org=(x_min, y_min - int(0.3 * text_height)),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.35,
        color=TEXT_COLOR,
        lineType=cv2.LINE_AA,
    )
    return img


def visualize(image, bboxes, category_ids, category_id_to_name, class_confidences):
    """

    :param image:
    :param bboxes: list, coco format
           e.g. [[586.23, 324.18, 16.15, 38.93]]
    :param category_ids: list
           e.g. [44]
    :param category_id_to_name: dict
           e.g. {1: 'person', 2: 'bicycle', 3: 'car', ...}
    :param class_confidences: list
           e.g. [0.76]
    :return:
    """
    img = image.copy()
    for bbox, category_id, class_confidence in zip(bboxes, category_ids, class_confidences):
        class_name = category_id_to_name[category_id]
        img = visualize_bbox(img, bbox, class_name, class_confidence)
    plt.figure(figsize=(12, 12))
    plt.axis('off')
    plt.imshow(img)
    # plt.show()
    plt.pause(1)
    plt.close()


def coco_to_yolo(bbox, width, height):
    """
    coco bbox -> yolo bbox
    [x_min, y_min, width, height] -> normalized [x_center, y_center, width, height]
    [98, 345, 322, 117] -> [0.4046875, 0.8613583, 0.503125, 0.24375]
    :param bbox: list, [x_min, y_min, width, height]
    :param width: int  the width px of the picture
    :param height: int  the height px of the picture
    :return: normalized [x_center, y_center, width, height]
    """
    x_min, y_min, coco_w, coco_h = bbox
    x_center = (x_min + coco_w / 2) / width
    y_center = (y_min + coco_h / 2) / height
    yolo_w = coco_w / width
    yolo_h = coco_h / height
    yolo_bbox = [x_center, y_center, yolo_w, yolo_h]
    return list(map(lambda x: round(x, 6), yolo_bbox))


def yolo_to_coco(bbox, width, height):
    """
    yolo bbox -> coco bbox
    normalized [x_center, y_center, width, height] -> [x_min, y_min, width, height]
    [0.4046875, 0.8613583, 0.503125, 0.24375] -> [98, 345, 322, 117]
    :param bbox: list, normalized [x_center, y_center, width, height]
    :param width: int  the width px of the picture
    :param height: int  the height px of the picture
    :return: [x_min, y_min, width, height]
    """
    x_center, y_center, yolo_w, yolo_h = bbox
    coco_w = yolo_w * width
    coco_h = yolo_h * height
    x_min = x_center * width - coco_w / 2
    y_min = y_center * height - coco_h / 2
    coco_bbox = [x_min, y_min, coco_w, coco_h]
    return list(map(lambda x: round(x), coco_bbox))


def roboflow_to_coco(bbox):
    """
    roboflow bbox -> coco bbox
    [x_center, y_center, width, height] -> [x_min, y_min, width, height]
    [334.0, 86.0, 28, 42] -> [320, 65, 28, 42]
    :param bbox: list, [x_center, y_center, width, height]
    :return: [x_min, y_min, width, height]
    """
    x_center, y_center, roboflow_w, roboflow_h = bbox
    coco_w = roboflow_w
    coco_h = roboflow_h
    x_min = x_center - coco_w / 2
    y_min = y_center - coco_h / 2
    coco_bbox = [x_min, y_min, coco_w, coco_h]
    return list(map(lambda x: round(x), coco_bbox))


if __name__ == '__main__':
    pass
