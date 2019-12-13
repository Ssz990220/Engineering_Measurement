import cv2
import functions
import numpy as np


def auto_exposure(src, mean):
    src_mean = np.mean(src)
    print(src_mean)
    auto_img = np.uint8(np.clip((src - (src_mean - mean)), 0, 255))
    return auto_img

tri1 = cv2.imread('2.bmp')
tri2 = cv2.imread('3.bmp')
tri3 = cv2.imread('4.bmp')
tri4 = cv2.imread('5.bmp')
tri5 = cv2.imread('6.bmp')

mean = 150
cv2.imshow('1',auto_exposure(tri1, mean))
cv2.imshow('2',auto_exposure(tri2, mean))
cv2.imshow('3',auto_exposure(tri3, mean))
cv2.imshow('4',auto_exposure(tri4, mean))
cv2.imshow('5',auto_exposure(tri5, mean))
cv2.waitKey()
cv2.destroyAllWindows()