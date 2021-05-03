# coding:utf8

"""
@author: Zhangao Lu
@contact:
@time: 2021/5/1
"""


import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from config.config import screen_shot_path, template_path


def get_axis_value(event, x, y, flags, param):
    """
    Get the axes' values of the position which is double-clicked.
    :param event:
    :param x:
    :param y:
    :param flags:
    :param param:
    :return:
    """
    if event == cv.EVENT_LBUTTONDBLCLK:
        print(x, y)


def draw_with_double_click():
    global img
    img = np.zeros((512, 512, 3), np.uint8)
    cv.namedWindow('image')
    cv.setMouseCallback('image', draw_circle)
    while (1):
        cv.imshow('image', img)
        if cv.waitKey(20) & 0xFF == 27:  # wait 20ms, exit if press Esc (ASCII No.27)
            break
    cv.destroyAllWindows()


def show_picture(img):
    cv.imshow('image', img)
    cv.waitKey(0)
    cv.destroyAllWindows()
 

def test_pictures():


    for j in range(1, 4):
        j = 4
        template = cv.imread(template_path + "fishing_float_%d.png" % 8)
        gray = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
        ret, template_thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
        w, h = template_thresh.shape[::-1]
        # show_picture(template_thresh)
        img = cv.imread(screen_shot_path + "1.%d.jpg" % j)
        # img = cv.imread(screen_shot_path + "2.jpg")

        # # Get the values of axes.
        # cv.namedWindow('image')
        # cv.setMouseCallback('image', get_axis_value)
        # while 1:
        #     cv.imshow('image', img)
        #     if cv.waitKey(20) & 0xFF == 27:
        #         break
        # cv.destroyAllWindows()
        #
        # x = 864
        # y = 211
        # half_length = 50
        # float_img = img[y-half_length: y+half_length, x-half_length: x+half_length]
        # show_picture(float_img)
        # cv.imwrite(template_path + 'fishing_float_8.png', float_img)



        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
        show_picture(thresh)

        res = cv.matchTemplate(thresh, template_thresh, cv.TM_CCOEFF_NORMED)
        print(res.shape)

        threshold = 0.6
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            cv.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        if loc[0].any():
            show_picture(img)
        break

        # dst = cv.adaptiveThreshold(binary_img, 200, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 3, 5)
        # show_picture(dst)

        # contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # 轮廓检测函数
        # cv.drawContours(thresh, contours, -1, (120, 0, 0), 2)  # 绘制轮廓
        # counter = 0
        # for cont in contours:
        #     rect = cv.boundingRect(cont)  # 提取矩形坐标
        #     print("x:{} y:{}".format(rect[0], rect[1]))  # 打印坐标
        #     cv.rectangle(img, rect, (0, 0, 0xff), 1)  # 绘制矩形
        #
        #     y = 10 if rect[1] < 10 else rect[1]  # 防止编号到图片之外
        #     counter += 1
        #     cv.putText(img, str(counter), (rect[0], y), cv.FONT_HERSHEY_COMPLEX, 0.4, (0, 255, 0), 1)  # 在米粒左上角写上编号
        # show_picture(img)
        # break


if __name__ == '__main__':
    # draw_with_double_click()
    test_pictures()


