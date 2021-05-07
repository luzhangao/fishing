# coding:utf8

"""
@author: Zhangao Lu
@contact:
@time: 2021/5/3
@description: The class used to control the mouse.
"""

import time
from pymouse import PyMouse


class MyPyMouse(object):
    def __init__(self):
        self.m = PyMouse()

    def move(self, x, y, sleep_time=0):
        """
        Move the mouse cursor.
        :param x: float
               The value of X-axis.
        :param y: float
               The value of Y-axis.
        :param sleep_time: float
               Sleep a short time to avoid move too fast..
        :return: None
        """
        self.m.move(x, y)
        time.sleep(sleep_time)

    def click(self, x, y, button, n, sleep_time=0):
        """
        Click the mouse
        :param x: float
               The value of X-axis.
        :param y: float
               The value of Y-axis.
        :param button: int
               Button is defined as 1 = left, 2 = right, 3 = middle.
        :param n: int
               Times need to click.
        :param sleep_time: float
               Sleep a short time to avoid move too fast.
        :return: None
        """
        self.m.click(x, y, button, n)
        time.sleep(sleep_time)

    def move_and_click(self, x, y, button, click_times, sleep_time_for_move, sleep_time_for_click):
        """
        Move and click the mouse.
        :param x: float
               The value of X-axis.
        :param y: float
               The value of Y-axis.
        :param button: int
               Button is defined as 1 = left, 2 = right, 3 = middle.
        :param click_times: int
               Times need to click.
        :param sleep_time_for_move: float
               Sleep a short time to avoid move too fast.
        :param sleep_time_for_click: float
               Sleep a short time to avoid move too fast.
        :return: None
        """
        # I found the center of the matched area is a bit upper left, so I balance the click point here.
        for elm in [9, 18]:
            new_x = x + elm
            new_y = y + elm
            self.move(new_x, new_y, sleep_time_for_move)
            self.click(new_x, new_y, button, click_times, sleep_time_for_click)
        time.sleep(0.5)


if __name__ == '__main__':
    pass
