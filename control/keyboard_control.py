# coding:utf8

"""
@author: Zhangao Lu
@contact:
@time: 2021/5/3
@description: The class used to press keys.
"""

import win32gui
from config.config import vkey


class MyPyKeyboard(object):
    def __init__(self, windows_hwnd):
        """
        :param windows_hwnd: window handle
               Get from win32gui.FindWindow(0, windows_name)
        """
        self.hwnd = windows_hwnd

    def press_key(self, key_name):
        """
        Press a single key
        :param key_name: string
        :return: None
        """
        win32gui.PostMessage(self.hwnd, vkey["key down"], vkey[key_name], 0)
        win32gui.PostMessage(self.hwnd, vkey["key up"], vkey[key_name], 0)

    def press_combo(self, key_name_1, key_name_2):
        """
        Press key 1 + key 2 at the same time.
        :param key_name_1: string
        :param key_name_2: string
        :return: None
        """
        win32gui.PostMessage(self.hwnd, vkey["key down"], vkey[key_name_1], 0)
        win32gui.PostMessage(self.hwnd, vkey["key down"], vkey[key_name_2], 0)
        win32gui.PostMessage(self.hwnd, vkey["key up"], vkey[key_name_2], 0)
        win32gui.PostMessage(self.hwnd, vkey["key up"], vkey[key_name_1], 0)


if __name__ == '__main__':
    pass
