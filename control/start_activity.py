# coding:utf8

"""
@author: Zhangao Lu
@contact:
@time: 2021/5/3
@description: The main function. It has two functions. If user press 1, it will save the template of floats. If user
 choose 2, it will go fishing.
key 4: fishing.
key 5: use the bait.
"""

import win32gui
import time
import multiprocessing
from multiprocessing import Process
from win32com import client
from control.keyboard_control import MyPyKeyboard
from control.match_template import MatchTemplate
from control.save_template import SaveTemplate


def start(windows_name="魔兽世界"):
    """

    :param windows_name: string
           "魔兽世界", "Wow of Warcraft"
    :return: None
    """
    is_full_screen = False  # If False, press Alt+Z.
    while 1:
        user_choice = input("选择1.生成鱼漂模板 2.钓鱼")
        if user_choice == "1":
            # Get the window and bring it to front.
            hwnd = win32gui.FindWindow(0, windows_name)
            shell = client.Dispatch("WScript.Shell")
            shell.SendKeys('%')
            mpk = MyPyKeyboard(hwnd)
            if not is_full_screen:  # If not, full screen.
                mpk.press_combo("ALT key", "Z key")
                is_full_screen = True
            mpk.press_key("4 key")  # key 4: fishing.
            time.sleep(2)  # Casting a fishing rod will cost almost 2 seconds.
            user_choice2 = input("按4调整鱼漂的位置直到找到一个满意的位置为止，按1截图")
            if user_choice2 == "1":
                print("在弹出的截图窗口种双击鱼漂的中心点，然后按ESC退出")
                # Save the template of fish float.
                st = SaveTemplate(hwnd)
                st.screen_shot()
                st.save()
            else:
                print("请按1截图")
        elif user_choice == "2":
            # Record the time of bait and use it every 10 minutes.
            bait_start_time = time.time()
            bait_end_time = time.time()
            time.sleep(1)
            hwnd = win32gui.FindWindow(0, windows_name)
            """
            Using "win32gui.SetForegroundWindow(hwnd)" only will cause an error 
            "pywintypes.error: (0, 'SetForegroundWindow', 'No error message is available')" in some cases.
            So add "shell" to avoid that, check:
            https://stackoverflow.com/questions/14295337/win32gui-setactivewindow-error-the-specified-procedure-could-not-be-found
            """
            shell = client.Dispatch("WScript.Shell")
            shell.SendKeys('%')
            # win32gui.SetForegroundWindow(hwnd)
            mpk = MyPyKeyboard(hwnd)
            mt = MatchTemplate(hwnd)
            if not is_full_screen:
                mpk.press_combo("ALT key", "Z key")
            mpk.press_key("5 key")  # key 5: use the bait.
            print("正在上鱼饵")
            time.sleep(6)  # It costs 5s to use the bait.
            cnt = 0
            while 1:
                cnt += 1
                if bait_end_time - bait_start_time >= 10 * 60:
                    mpk.press_key("5 key")
                    print("正在上鱼饵")
                    time.sleep(6)  # It spent 5s to use the bait.
                    bait_start_time = time.time()
                else:
                    bait_end_time = time.time()
                mpk.press_key("4 key")
                time.sleep(1)
                tf, xl, yl = mt.match_all()  # Take a screen shot and compare it with all float templates
                """
                If any float template can be found in the screen shot, keep matching it. If the float template can not 
                be found in the latest screen shot, it means the fish bites the bait. However, each loop will cost 
                almost 1s which is much longer than the time for biting the bait. So if there is only one process, the 
                failure rate is very high. Hence, I used 3 processes in one second here.
                """
                if tf and xl.any() and yl.any():
                    quits = multiprocessing.Event()
                    foundit = multiprocessing.Event()
                    for i in range(1, 4):
                        p = Process(target=mt.match, args=(tf, xl, yl, "temp_screenshot_%d.png" % i, quits, foundit, str(i)))
                        p.start()
                        time.sleep(0.3)
                    # mt.match(ft, xl, yl)
                    foundit.wait()
                    quits.set()
                time.sleep(2)
        else:
            print("输入不正确，请重新输入！")


if __name__ == '__main__':
    start()

