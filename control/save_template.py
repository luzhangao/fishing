# coding:utf8

"""
@author: Zhangao Lu
@contact:
@time: 2021/5/2
Save the template (fishing float) chosen by the user
"""

import os
import win32con
import win32gui
import time
import cv2 as cv
from PIL import ImageGrab
from config.config import temp_path, template_path


class SaveTemplate(object):
    def __init__(self, windows_hwnd):
        """

        :param windows_hwnd: window handle
               Get from win32gui.FindWindow(0, windows_name)
        """
        self.x = 0  # The value of X-axis.
        self.y = 0  # The value of Y-axis.
        self.half_range = 40  # img[y-half_range: y+half_range, x-half_range: x+half_range]
        self.hwnd = windows_hwnd
        self.temp_screenshot = "temp_screenshot.png"  # File name to save the temporary screen shot.

    def get_axis_value(self, event, x, y, flags, param):
        """
        Get the axes' values of the position which is double-clicked.
        :param event:
        :param x: int
               The value of X-axis.
        :param y: int
               The value of Y-axis.
        :param flags:
        :param param:
        :return: None
        """
        if event == cv.EVENT_LBUTTONDBLCLK:  # If event = Double click the left button of the mouse.
            self.x = x
            self.y = y

    def screen_shot(self):
        """
        Take a screen shot and save the picture.
        :return: None
        """
        win32gui.SetForegroundWindow(hwnd)  # Put the window in foreground.
        time.sleep(0.7)
        img = ImageGrab.grab()
        img.save(temp_path + self.temp_screenshot, 'png')

    def save(self):
        """
        Save what user choose to the "template" folder.
        :return: None
        """
        img = cv.imread(temp_path + self.temp_screenshot)
        cv.namedWindow('image')
        cv.setMouseCallback('image', self.get_axis_value)
        while 1:
            cv.imshow('image', img)
            if cv.waitKey(20) & 0xFF == 27:  # Press Esc to quit.
                break
        cv.destroyAllWindows()
        # Cut the area what the user choose.
        float_img = img[self.y - self.half_range: self.y + self.half_range,
                    self.x - self.half_range: self.x + self.half_range]
        cv.imwrite(template_path + self.picture_name(), float_img)  # Save the cut part to the "template" folder.

    @staticmethod
    def picture_name():
        """
        Genarate the name of the picture. The name should be like 1.png, 2.png, ..., n.png.
        :return: string
                 "x.png"
        """
        file_list = list()  # Used to store all the exist files.
        for _, _, files in os.walk(template_path):
            file_list.extend(files)
        if file_list:
            # ["1.png", "2.png", ..., "n.png"] --> [1, 2, ..., n] --> max([1, 2, ..., n])
            max_value = max(map(lambda x: int(x[: len(x)-4]), file_list))
            return "%d.png" % (max_value + 1)
        else:  # If there is no files in this folder, use "1.png"
            return "1.png"


if __name__ == '__main__':
    windows_name = "魔兽世界"
    hwnd = win32gui.FindWindow(0, windows_name)
    print("hwnd", hwnd)
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    st = SaveTemplate(hwnd)
    st.screen_shot()
    st.save()
    print(st.x, st.y)
