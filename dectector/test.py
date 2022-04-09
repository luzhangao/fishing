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


# windows_name = "魔兽世界"
# hwnd = win32gui.FindWindow(0, "Desktop")

hwnd = win32gui.GetDesktopWindow()
print("hwnd", hwnd)
left, top, right, bottom = win32gui.GetWindowRect(hwnd)

bounding_box = {'top': top, 'left': left, 'width': right, 'height': bottom}

sct = mss()

while True:
    sct_img = sct.grab(bounding_box)
    print(np.array(sct_img).shape)
    cv2.imshow('screen', np.array(sct_img))

    scr_img = model(scr_img)
    cv2.imshow('Testing', scr_img)

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break


