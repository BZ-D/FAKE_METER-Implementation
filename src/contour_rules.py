# coding=UTF-8
import cv2.cv2 as cv

# param c is an instance of class Contour


def is_too_small(c):
    """
    rule1
    c.h < 10 or c.w < 10
    """
    return c.h < 10 or c.w < 10


def is_too_large(c, H, W):
    """
    rule2
    c.h > 0.75H or
    c.w > 0.75W or
    c.h * c.w > 0.75 H*W
    where H is the height of screen
          W is the width of screen
    """
    return c.h > 0.75 * H or c.w > 0.75 * W or c.h * c.w > 0.75 * H * W

def is_too_slim(c):
    """
    rule3
    c.w / c.h < 0.1
    """
    return c.w / c.h < 0.1


def is_too_fat(c):
    """
    rule4
    c.h / c.w < 0.1
    """
    return c.h / c.w < 0.1


def is_covered(c, C):
    """
    rule5
    C is a set of instances of Contour
    ∃c' ∈ C:
    (c ∩ c').area / c'.area > 0.8
    &&
    c'.area > c.area
    """
    c_area = cv.contourArea(c)
    for cc in C:

        cc_area = cv.contourArea(cc)
        if c_area < cc_area and ((c_area - cc_area) / cc_area > 0.8 or (cc_area - c_area) / cc_area > 0.8):
            return True

    return False