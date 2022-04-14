# coding:utf8

"""
@author: Zhangao Lu
@contact: zlu2@laurentian.ca
@time: 2022/4/7
@description:
"""

import numpy as np
import cv2
from mss import mss
from PIL import Image
from win32 import win32gui, win32api
import os
import torch


# Model
model = torch.hub.load(r'yolov5', 'custom', path=r'models\best.pt', source='local')


# windows_name = "魔兽世界"
# hwnd = win32gui.FindWindow(0, "Desktop")

hwnd = win32gui.GetDesktopWindow()
print("hwnd", hwnd)
left, top, right, bottom = win32gui.GetWindowRect(hwnd)

bounding_box = {'top': top, 'left': left, 'width': right, 'height': bottom}

sct = mss()

while True:
    sct_img = sct.grab(bounding_box)

    scr_img = np.array(sct_img)
    #cv2.imshow('screen', scr_img) # display screen in box

    scr_img = model(scr_img)

    scr_img.print()
    # scr_img.show()

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break
