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
    for pred in scr_img.pred:
        print(pred.cpu().numpy())

    # scr_img.print()
    # print(dir(scr_img))
    # for attr in dir(scr_img):
    #     print(f"{attr}", eval(f"scr_img.{attr}"))
    # print(scr_img.xyxyn)
    # print(scr_img.xyxyn[0])
    # labels, cord_thres = scr_img.xyxyn[0][:, -1].numpy(), scr_img.xyxyn[0][:, :-1].numpy()
    # print(labels, cord_thres)

    # scr_img.show()


    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break
