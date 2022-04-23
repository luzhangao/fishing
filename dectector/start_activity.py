# coding:utf8

"""
@author: Zhangao Lu
@contact:
@time: 2022/4/23
@description:
key 4: fishing.
key 5: use the bait.
"""
import sys
sys.path.append("../")

import win32gui
import time
import random
import torch
import numpy as np
from win32com import client
from mss import mss
from control.mouse_control import MyPyMouse
from control.keyboard_control import MyPyKeyboard
from control.match_template import MatchTemplate


def random_action(hwnd, cnt):
    """
    Do some random actions to avoid log out.
    :param hwnd: window handle
           Get from win32gui.FindWindow(0, windows_name)
    :param cnt: int
    :return: None
    """
    mpk = MyPyKeyboard(hwnd)
    if cnt % 10000 == 9:
        random_choice = random.randint(1, 5)
        if random_choice == 1:
            # mpk.press_key("space key")
            pass
        elif random_choice == 2:
            # mpk.press_key("3 key")
            pass
        elif random_choice == 3:
            mpk.press_key("6 key")
            time.sleep(0.5)
        else:
            mpk.press_key("6 key")
            time.sleep(0.5)
    else:
        time.sleep(0.5)


def start(windows_name="魔兽世界"):
    """

    :param windows_name: string
           "魔兽世界", "Wow of Warcraft"
    :return: None
    """
    is_full_screen = False  # If False, press Alt+Z.
    model = torch.hub.load(r'yolov5', 'custom', path=r'models\best.pt', source='local')
    sct = mss()
    while True:
        # Record the time of bait and use it every 10 minutes.
        bait_start_time = time.time()
        bait_end_time = time.time()
        time.sleep(1)
        hwnd = win32gui.FindWindow(0, windows_name)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        bounding_box = {'top': top, 'left': left, 'width': right, 'height': bottom}
        print(bounding_box)

        shell = client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(hwnd)

        mpk = MyPyKeyboard(hwnd)
        mpm = MyPyMouse()
        mt = MatchTemplate(hwnd)
        if not is_full_screen:
            mpk.press_combo("ALT key", "Z key")

        mpk.press_key("5 key")  # key 5: use the bait.
        print("Using bait.")
        time.sleep(6)  # It costs 5s to use the bait.

        cnt = 0
        fishing_start_time = time.time()
        while 1:
            cnt += 1
            random_action(hwnd, cnt)
            if bait_end_time - bait_start_time >= 10 * 60 + 10:
                mpk.press_key("5 key")
                print("Using bait.")
                time.sleep(7)  # It spent 5s to use the bait.
                print("Bait is used.")
                bait_start_time = time.time()
            else:
                bait_end_time = time.time()

            sct_img = sct.grab(bounding_box)
            scr_img = np.array(sct_img)
            scr_img = model(scr_img)
            if time.time() - fishing_start_time >= 3:
                for pred in scr_img.pred:
                    # [[     978.93      183.25      1057.7      276.18     0.74201           0]
                    #  [      976.1      167.86      1058.9      283.29     0.25981           1]]
                    pred = pred.cpu().numpy()
                    print(pred)
                    if pred.size > 0:  # Check if pred is empty or not.
                        # Ensure that the threshold of caught float is greater than the threshold of normal fishing float.
                        max_values = np.argmax(pred, axis=0)  # e.g. [0 0 1 1 0 1]
                        if pred[max_values[4], 5] == 1:
                            for row in pred:
                                # [x_min, y_min, x_max, y_max, threshold, class_id]
                                # [     978.93      183.25      1057.7      276.18     0.74201           0]
                                if row[4] >= 0.7 and row[5] == 1:
                                    # Compute the center of bbox
                                    x = int((row[0] + row[2]) / 2)
                                    y = int((row[1] + row[3]) / 2)
                                    mpm.move(x, y)
                                    time.sleep(0.2)
                                    mpm.click(x, y, 2, 1)
                                    print("click!")
                                    time.sleep(0.5)
                                    # if len(positive_list) >= 2:
                                    #     mpm.move(x, y)
                                    #     mpm.click(x, y, 2, 1)
                                    #     time.sleep(0.5)
                                    #     positive_list = list()
                    else:
                        mpk.press_key("4 key")
                        fishing_start_time = time.time()
                        time.sleep(1)
            continue
            time.sleep(0.5)


if __name__ == '__main__':
    start()


