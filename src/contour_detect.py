import cv2.cv2 as cv
import numpy as np


def draw_contours(img, cnts):
    # cnts = contours
    img = np.copy(img)

    # -1: draw all contours;
    # (0, 255, 0): color of contour;
    # 2: line width of drawn contour
    img = cv.drawContours(img, cnts, -1, (0, 255, 0), 2)

    return img


def draw_min_rect_circle(img, cnts):
    # cnts = contours
    # draw a minimal rectangle to cover the detected shape

    img = np.copy(img)
    for cnt in cnts:
        # cv2.boundingRect(cnt)
        # find the bounding rect of img
        # cnt : a set of contour points, which can be gotten by cv2.findContours()
        # return : (x,y) - the coordinates of upper left point
        #           w,h  - the width and height of rect
        x, y, w, h = cv.boundingRect(cnt)

        # draw the bounding rect
        # (x+w,y+h): the coordinates of lower right point
        cv.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)  # red

        # cv2.minAreaRect(cnt)
        # find the minimal bounding rect of img
        min_rect = cv.minAreaRect(cnt)

        # cv2.boxPoints(points)
        # get four coordinates of a rect
        # return : clockwise four coordinates
        min_rect = np.int64(cv.boxPoints(min_rect))
        cv.drawContours(img, [min_rect], 0, (0,255,0), 2)  # green

        # get minimal enclosing circle
        (x,y), radius = cv.minEnclosingCircle(cnt)
        center, radius = (int(x), int(y)), int(radius)
        img = cv.circle(img, center, radius, (0,0,255), 2)  # red

        return img


def draw_approx_hull_polygon(img, cnts):
    img = np.zeros(img.shape, dtype=np.uint8)
    cv.drawContours(img, cnts, -1, (255,0,0), 2)

    # the minimum side len of polygon
    min_side_len = img.shape[0] / 32
    # the minimum round len of polygon
    min_poly_len = img.shape[0] / 16
    # the minimum of polygon's sides
    min_side_num = 3

    # use min_side_len as limit to draw a polygon
    approxs = [cv.approxPolyDP(cnt, min_side_len, True) for cnt in cnts]
    # filter the polygons whose round len larger than min_poly_len
    approxs = [approx for approx in approxs if cv.arcLength(approx, True) > min_poly_len]
    # filter the polygons whose side number larger than min_side_num
    approxs = [approx for approx in approxs if len(approx) > min_side_num]

    # draw the polygon
    cv.polylines(img, approxs, True, (0,255,0), 2)

    hulls = [cv.convexHull(cnt) for cnt in cnts]
    cv.polylines(img, hulls, True, (0,0,255), 2)

    return img


def run():
    # add img and change it into binary img
    # notice that the img read is like (B,G,R)
    image = cv.imread("01.png")
    # using Canny Algorithm to extract the edge of img
    # 128: threshold1, used to connect discontinuous edges
    # 256: threshold2, used to detect obvious contour
    thresh = cv.Canny(image, 128, 256)
    # find all contours
    contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    imgs = [
        image,
        draw_min_rect_circle(image, contours),
        draw_approx_hull_polygon(image, contours)
    ]

    for img in imgs:
        # make the window stretchable
        cv.namedWindow('contours', cv.WINDOW_NORMAL)
        cv.imshow('contours', img)
        cv.waitKey()


if __name__ == '__main__':
    run()

pass