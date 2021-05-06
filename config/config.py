# coding:utf8

"""
@author: Zhangao Lu
@contact:
@time: 2021/4/26
@description:
"""

import win32con


template_path = "../data/template/"  # A file folder to save all the fish float templates.
temp_path = "../data/temp/"  # A temporary file folder to save the screen shots.

match_threshold = 0.6  # The rate used in matching between the screen shot and fish float templates.


# virtual key codes, for short, vkey
# https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
# https://docs.microsoft.com/en-us/windows/win32/inputdev/mouse-input
vkey = {
    "key down": win32con.WM_KEYDOWN,
    "key up": win32con.WM_KEYUP,

    "0 key": 0x30,
    "1 key": 0x31,
    "2 key": 0x32,
    "3 key": 0x33,
    "4 key": 0x34,
    "5 key": 0x35,
    "6 key": 0x36,
    "7 key": 0x37,
    "8 key": 0x38,
    "9 key": 0x39,

    "Z key": 0x5A,
    "ALT key": 0x12,
    "space key": 0x20,

    "left mouse down": win32con.WM_LBUTTONDOWN,
    "left mouse up": win32con.WM_LBUTTONUP,
    "right mouse down": win32con.WM_RBUTTONDOWN,
    "right mouse up": win32con.WM_RBUTTONUP,
    "left mouse button": win32con.MK_LBUTTON,
    "right mouse button": win32con.MK_RBUTTON,
}


if __name__ == '__main__':
    pass
