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

    "A key": 0x41,
    "B key": 0x42,
    "C key": 0x43,
    "D key": 0x44,
    "E key": 0x45,
    "F key": 0x46,
    "G key": 0x47,
    "H key": 0x48,
    "I key": 0x49,
    "J key": 0x4A,
    "K key": 0x4B,
    "L key": 0x4C,
    "M key": 0x4D,
    "N key": 0x4E,
    "O key": 0x4F,
    "P key": 0x50,
    "Q key": 0x51,
    "R key": 0x52,
    "S key": 0x53,
    "T key": 0x54,
    "U key": 0x55,
    "V key": 0x56,
    "W key": 0x57,
    "X key": 0x58,
    "Y key": 0x59,
    "Z key": 0x5A,
    "ALT key": 0x12,
    "space key": 0x20,

    "left windows key": 0x5B,
    "right windows key": 0x5C,

    "left menu key": 0xA4,
    "right menu key": 0xA4,

    "caps lock key": 0x14,
    "PRINT SCREEN key": 0x2C,


    "left mouse down": win32con.WM_LBUTTONDOWN,
    "left mouse up": win32con.WM_LBUTTONUP,
    "right mouse down": win32con.WM_RBUTTONDOWN,
    "right mouse up": win32con.WM_RBUTTONUP,
    "left mouse button": win32con.MK_LBUTTON,
    "right mouse button": win32con.MK_RBUTTON,
}


START_FISHING_SLEEP_TIME = 2  # Skip the first x second to reduce false positive rate
MOVE_MOUSE_SLEEP_TIME = 0.2  # Add some sleep time to avoid moving mouse too fast
CLICK_MOUSE_SLEEP_TIME = 0.5  # Add some sleep time to avoid clicking mouse too fast
GENERAL_SLEEP_TIME = 1  # Sleep time for other cases
BITE_SLEEP_TIME = 5 + 1  # It costs 5s to use the bait


if __name__ == '__main__':
    pass
