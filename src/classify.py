import contour_rules as rules
import cv2.cv2 as cv


def v_difference(c1, c2):
    c1_x, c1_y, w1, h1 = cv.boundingRect(c1)
    c2_x, c2_y, w2, h2 = cv.boundingRect(c2)
    return abs(c1_y - c2_y)


def h_distance(c1, c2):
    c1_x, c1_y, w1, h1 = cv.boundingRect(c1)
    c2_x, c2_y, w2, h2 = cv.boundingRect(c2)
    return abs(c1_x - c2_x)


def is_text(c, words):
    # to judge whether a contour belongs to text
    # c: contour ; words: words_result from OCR

    for word in words:
        content = word['words']
        left, top = word['location']['left'], word['location']['top']

        # (c_x, c_y) is the coordinates of contour
        c_x, c_y, w, h = cv.boundingRect(c)

        if rules.is_too_fat(c) or rules.is_too_slim(c) or rules.is_too_small(c) or rules.is_too_large(c, w, h):
            # satisfying any of the contour_rules
            return 'illegal contour!'

        else:
            # classifying the elements
            if abs(left - c_x) <= 5 and abs(top - c_y) <= 5:
                # adjacent
                return True

    return False
