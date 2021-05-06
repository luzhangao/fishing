# coding:utf8

"""
@author: Zhangao Lu
@contact:
@time: 2021/5/3
@description: Take a screen shot and match the template floats.
"""

import time
import numpy as np
import cv2 as cv
import win32gui
from control.save_template import SaveTemplate
from control.mouse_control import MyPyMouse
from config.config import temp_path, template_path, match_threshold


class MatchTemplate(SaveTemplate):
    def __init__(self, windows_hwnd):
        """

        :param windows_hwnd: window handle
               Get from win32gui.FindWindow(0, windows_name)
        """
        super().__init__(windows_hwnd)
        super().picture_name()
        # Compute the time current fishing costs. If the time > 30, restart fishing.
        self.start_time = 0
        self.end_time = 0

    @staticmethod
    def gray(img):
        """
        Use to convert the picture from BRG to gray. It has been abandoned.
        :param img: retval
               the image object in opencv
        :return: dst
        """
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
        return thresh

    @staticmethod
    def display_picture(img):
        """

        :param img: retval
               the image object in opencv
        :return: None
        """
        cv.imshow('image', img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def get_screen_shot(self, picture_name=""):
        """
        :param picture_name: string
               The name of the picture.
        :return: None
        """
        self.screen_shot(picture_name=picture_name)
        if not picture_name:
            self.img = cv.imread(temp_path + self.temp_screenshot)
        else:
            self.img = cv.imread(temp_path + picture_name)

    def match_all(self):
        """
        Compare all templates at first, then choose the most reliable one
        :return: final_tf, string
                 Template file name
                 xl, np.array()
                 The array of values of X-axis
                 yl, np.array()
                 The array of values of Y-axis
        """
        self.start_time = time.time()
        self.get_screen_shot()

        xl = np.array([])
        yl = np.array([])

        final_tf = ""

        for tf in self.file_list:  # Match every fishing float template.
            template = cv.imread(template_path + tf)  # Read fishing float template.
            # res = cv.matchTemplate(self.gray(img), self.gray(template), cv.TM_CCOEFF_NORMED)  # It has been abandoned.
            # Match the screen shot with the float template.
            res = cv.matchTemplate(self.img, template, cv.TM_CCOEFF_NORMED)
            loc = np.where(res >= match_threshold)  # loc = (np.array, np.array)
            if loc[0].any():  # If the array is not null, it means the template is matched.
                # self.display_picture(img)
                if not xl.any():
                    xl = loc[1]
                    yl = loc[0]
                    final_tf = tf
                else:
                    # If there is more than one template matched,
                    # choose the one with the largest amount of matched pixels.
                    if len(loc[1]) > len(xl) or len(loc[0]) > len(yl):
                        xl = loc[1]
                        yl = loc[0]
                        final_tf = tf
        return final_tf, xl, yl

    def match(self, tf, xl, yl, picture_name, thread_name, stop_thread):
        """
        Match the screen shot with the chosen template in a loop until catch the fish or the time is more than 30s.
        :param tf: string
               The name of chosen template.
        :param xl: np.array
               The axis of matched pixels.
        :param yl: np.array
               The axis of matched pixels.
        :param picture_name: string
               The name of the picture, used to debug the code.
        :param thread_name: string
               The name of the process, used to debug the code.
        :param stop_thread: multiprocessing.Event()
               Used to communicate between processes.
        :return:
        """
        raw_x = np.median(xl)
        raw_y = np.median(yl)
        # raw_x = (np.max(xl)+np.min(xl))/2
        # raw_y = (np.max(xl)+np.min(yl))/2
        x = int(raw_x)
        y = int(raw_y)
        """
        Used to compute the mean of elements numbers of loc[0] or loc[1]. If this mean changes rapidly, it means 
        the fish gets hooked.
        """

        elements_number_list = list()
        is_find_fish = False
        is_time_over = False
        print("Start thread %s" % thread_name)
        while not stop_thread.is_set():
            self.get_screen_shot(picture_name)
            template = cv.imread(template_path + tf)  # Read fishing float template.
            # res = cv.matchTemplate(self.gray(img), self.gray(template), cv.TM_CCOEFF_NORMED)
            res = cv.matchTemplate(self.img, template, cv.TM_CCOEFF_NORMED)
            loc = np.where(res >= match_threshold)
            elements_number_list.append(len(loc[0]))
            # print(len(loc[0]), len(loc[1]), len(xl), len(loc[0]) / np.mean(elements_number_list))
            # print("--------------", tf, x, y)
            if len(loc[0]) / np.mean(elements_number_list) <= 0.6:
                print("Thread %s find the fish, catch" % thread_name)
                mpm = MyPyMouse()
                mpm.move_and_click(x=x, y=y, button=2, click_times=1, sleep_time_for_move=0.1,
                                   sleep_time_for_click=0.1)
                stop_thread.set()
                is_find_fish = True
            self.end_time = time.time()
            if self.end_time - self.start_time >= 30:
                print("Thread %s already 30s" % thread_name)
                mpm = MyPyMouse()
                mpm.move_and_click(x=x, y=y, button=2, click_times=1, sleep_time_for_move=0.1,
                                   sleep_time_for_click=0.1)
                stop_thread.set()
                is_time_over = True
        if not is_find_fish and not is_time_over:
            print("Thread % s receive the signal to stop the thread" % thread_name)


if __name__ == '__main__':
    pass

