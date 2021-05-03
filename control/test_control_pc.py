# coding:utf8

"""
@author: Zhangao Lu
@contact:
@time: 2021/4/27
"""

import time
# import uiautomation as automation
import random
import win32ui
import win32gui, win32api
import win32con
import numpy as np
from pymouse import PyMouse, PyMouseEvent
from pykeyboard import PyKeyboard
from config.config import vkey


def test():
    windows_name = "魔兽世界"
    # windows_name = "World of Warcraft"
    # windows_name = "*new 1 - Notepad++"
    hwnd = win32gui.FindWindow(0, windows_name)
    print("hwnd", hwnd)
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)

    win32gui.SetForegroundWindow(hwnd)  # 将窗口最前显示
    print(win32api.GetCursorPos())  # print the position of the mouse
    cnt = 0
    while 1:
        cnt += 1
        win32gui.PostMessage(hwnd, vkey["key down"], vkey["4 key"], 0)  # press
        win32gui.PostMessage(hwnd, vkey["key up"], vkey["4 key"], 0)  # release
        time.sleep(2)
        win32gui.PostMessage(hwnd, vkey["left mouse down"], vkey["left mouse button"], 0)
        win32gui.PostMessage(hwnd, vkey["left mouse up"], vkey["left mouse button"], 0)
        time.sleep(1)



if __name__ == '__main__':
    test()


