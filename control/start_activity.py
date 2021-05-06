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
import random
import threading
import concurrent
from concurrent.futures import ThreadPoolExecutor
from win32com import client
from control.mouse_control import MyPyMouse
from control.keyboard_control import MyPyKeyboard
from control.match_template import MatchTemplate
from control.save_template import SaveTemplate


def random_action(hwnd, cnt):
    """
    Do some random actions to avoid log out.
    :param hwnd: window handle
           Get from win32gui.FindWindow(0, windows_name)
    :param cnt: int
    :return: None
    """
    if cnt % 100 == 0 or cnt % 100 == 3:
        mpk = MyPyKeyboard(hwnd)
        random_choice = random.randint(1, 4)
        if random_choice == 1:
            mpk.press_key("space key")
        elif random_choice == 2:
            mpk.press_key("3 key")
        else:
            pass


def start(windows_name="魔兽世界"):
    """

    :param windows_name: string
           "魔兽世界", "Wow of Warcraft"
    :return: None
    """
    is_full_screen = False  # If False, press Alt+Z.
    while 1:
        user_choice = input("Choose 1.Generate fish float template 2.Fishing")
        if user_choice == "1":
            # Get the window and bring it to front.
            hwnd = win32gui.FindWindow(0, windows_name)
            shell = client.Dispatch("WScript.Shell")
            shell.SendKeys('%')
            win32gui.SetForegroundWindow(hwnd)
            mpk = MyPyKeyboard(hwnd)
            if not is_full_screen:  # If not, full screen.
                mpk.press_combo("ALT key", "Z key")
                is_full_screen = True
            mpk.press_key("4 key")  # key 4: fishing.
            time.sleep(2)  # Casting a fishing rod will cost almost 2 seconds.
            user_choice2 = input("Press 4 until the fish float locate in a perfect place, "
                                 "then press 1 take the screen shoot.")
            if user_choice2 == "1":
                print("Double click the center of the fish float in the pop-up window. Then press ESC to exit.")
                # Save the template of fish float.
                st = SaveTemplate(hwnd)
                st.screen_shot()
                st.save()
            else:
                print("Please press 1 to take a screen shoot.")
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
            while 1:
                cnt += 1
                random_action(hwnd, cnt)
                if bait_end_time - bait_start_time >= 10 * 60:
                    mpk.press_key("5 key")
                    print("Using bait.")
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
                almost 1s which is much longer than the time for biting the bait. So if there is only one 
                process or thread, the failure rate is very high. Hence, I used 3 threads in one second here.
                """
                if tf and xl.any() and yl.any():
                    futures = list()
                    with ThreadPoolExecutor(max_workers=3) as executor:
                        stop_thread = threading.Event()
                        for i in range(1, 4):
                            future = executor.submit(mt.match, tf, xl, yl, "temp_screenshot_%d.png" % i, str(i), stop_thread)
                            time.sleep(0.3)
                            futures.append(future)
                        # Handle each one as soon as it’s ready, even if they come out of order.
                        # https://stackoverflow.com/questions/52082665/store-results-threadpoolexecutor
                        futures, _ = concurrent.futures.wait(futures)
                        for future in futures:
                            result = future.result()
                            x = result[0]
                            y = result[1]
                            if x and y:
                                """
                                At first, move and click the mouse was called in the method match(). However, when the
                                threads find the float missing in the same time. They both call move_and_click(), and 
                                that will cause the mouse moves unexpectedly. To solve this, I collect the returned 
                                values of the mouse cursor. Then call move_and_click() only once now.
                                """
                                mpm.move_and_click(x=x, y=y, button=2, click_times=1, sleep_time_for_move=0.1,
                                                   sleep_time_for_click=0.1)
                time.sleep(1)
        else:
            print("Wrong number, please type it again.")


if __name__ == '__main__':
    start()

