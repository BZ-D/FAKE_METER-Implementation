# -*- coding: utf-8 -*-

import cv2.cv2
import os
import numpy as np

"""
计算图片是否是护眼模式/黑暗模式下的图片
通过计算所有像素点RGB的平均值
如果是，则将其转换为负片后再传给OCR进行轮廓提取
"""


def compute(filepath):
    img = cv2.imread(filepath, 1)

    DARK_MODE_THRESHOLD = 150

    # 注意：imread读出的是 BGR 形式

    # cv2.imread() 返回值类型：np.array
    # [:,:,0] - 取三维数组的第一维所有元素，即所有像素点的蓝色值
    Bmean = np.mean(img[:, :, 0])

    # [:,:,1] - 取三维数组的第二维所有元素，即所有像素点的绿色值
    Gmean = np.mean(img[:, :, 1])

    # [:,:,2] - 取三维数组的第三维所有元素，即所有像素点的红色值
    Rmean = np.mean(img[:, :, 2])

    # 计算图片上所有像素点的RGB均值
    BGR_mean = np.average([Bmean, Gmean, Rmean])

    if BGR_mean < DARK_MODE_THRESHOLD:
        # 平均 rgb 值小于阈值 150
        img = cal_complement_img(img)
        cv2.imshow("complement img", img)
        cv2.waitKey()

    return img


# high time cost !!
def cal_complement_img(img):
    h, w, channels = img.shape[0:3]
    for row in range(h):
        for col in range(w):
            for c in range(channels):
                pixel = img[row, col, c]
                img[row, col, c] = 255 - pixel
    return img


if __name__ == '__main__':
    compute('02.png')
