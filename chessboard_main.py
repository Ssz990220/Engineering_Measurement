import cv2
import functions
from collections import Counter
import numpy as np


width = 900
height = 600
mean = 150
chs_src = cv2.imread('.\\chessboard\\000.bmp')
gray = cv2.cvtColor(chs_src, cv2.COLOR_BGR2GRAY)
# chs_auto, src_mean = functions.auto_exposure(gray, mean, False)
# cv2.imshow('auto', chs_auto)
# cv2.waitKey()
# threshold = (src_mean - 150) * (125 / 70)       ####需要标定！！！
# print(threshold)
ratio = chs_src.shape[0] / chs_src.shape[1]
'''
自动曝光调试
'''
cv2.namedWindow('thresh_test',cv2.WINDOW_NORMAL)
cv2.resizeWindow('thresh_test',width, int(width*ratio))

def update(x):
    pass


cv2.createTrackbar('upper', 'thresh_test', 0, 255, update)
cv2.createTrackbar('lower', 'thresh_test', 0, 255, update)

while (1):
    k = cv2.waitKey(1)
    if k == ord('e'):
        break
    upper = cv2.getTrackbarPos('upper', 'thresh_test')
    lower = cv2.getTrackbarPos('lower', 'thresh_test')
    ret, img = cv2.threshold(gray, lower, upper, cv2.THRESH_BINARY)
    cv2.namedWindow('thresh_test',0)
    cv2.resizeWindow('thresh_test',width,height)
    cv2.imshow('thresh_test', img)

cv2.namedWindow('origin', 0)
cv2.resizeWindow('origin', width, height)
cv2.namedWindow('auto_exposure', 0)
cv2.resizeWindow('auto_exposure', width, height)
cv2.imshow('origin', gray)
cv2.imshow('auto_exposure', gray)
cv2.waitKey()
cv2.destroyAllWindows()

'''
阈值处理
'''

ret, thresh_img = cv2.threshold(gray,100,255, cv2.THRESH_BINARY)
black_area = sum(sum(thresh_img==0))                    #通过黑色的面积得知相机到平面的距离
upper_thresh = black_area/(thresh_img.shape[0]*thresh_img.shape[1])            ##需要标定
cv2.namedWindow('thresh_img',0)
cv2.resizeWindow('thresh_img', width,height)
cv2.imshow('thresh_img', thresh_img)
cv2.waitKey()


'''
边缘检测调试
'''
# cv2.namedWindow('canny_test', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('canny_test', 1500,1200)
#
#
# def update(x):
#     pass
#
#
# cv2.createTrackbar('upper', 'canny_test', 1, 255, update)
# cv2.createTrackbar('lower', 'canny_test', 1, 255, update)
#
# while (1):
#     k = cv2.waitKey(1)
#     if k == ord('e'):
#         break
#     cp = thresh_img.copy()
#     upper = cv2.getTrackbarPos('upper', 'canny_test')
#     lower = cv2.getTrackbarPos('lower', 'canny_test')
#     edges = cv2.Canny(cp, lower, upper)
#     cv2.imshow('canny_test', edges)

'''
边缘提取
'''
edges = cv2.Canny(thresh_img, 150, 200)

cv2.namedWindow('edges',0)
cv2.resizeWindow('edges',width,height)
cv2.imshow('edges',edges)

'''
霍夫直线调试
'''
def nothing(x):
    pass


masked_src_lines = edges.copy()
cv2.namedWindow('test', 0)
cv2.resizeWindow('test', width,height+200)
cv2.createTrackbar('angle_resolution', 'test', 1, 720, nothing)
cv2.createTrackbar('rho', 'test', 1, 100, nothing)
cv2.createTrackbar('threshold', 'test', 1, 200, nothing)
cv2.createTrackbar('minlinelength', 'test', 1, 500, nothing)
cv2.createTrackbar('minlinegap', 'test', 1, 500, nothing)
cv2.setTrackbarPos('rho', 'test', 50)
cv2.setTrackbarPos('angle_resolution', 'test', 360)
cv2.setTrackbarPos('threshold', 'test', 140)
cv2.setTrackbarPos('minlinelength', 'test', 500)
cv2.setTrackbarPos('minlinegap', 'test', 150)
while (1):
    k = cv2.waitKey(1)
    if k == ord('e'):
        break
    cv2.imshow('test', masked_src_lines)
    masked_src_lines = chs_src.copy()
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    angle_resolution = int(cv2.getTrackbarPos('angle_resolution', 'test'))
    theta = np.pi / angle_resolution
    rho = cv2.getTrackbarPos('rho', 'test') / 50
    threshold = int(cv2.getTrackbarPos('threshold', 'test'))
    minlinelength = int(cv2.getTrackbarPos('minlinelength', 'test'))
    minlinegap = int(cv2.getTrackbarPos('minlinegap', 'test'))
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, minLineLength=minlinelength, maxLineGap=minlinegap)
    try:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(masked_src_lines, (x1, y1), (x2, y2), (0, 0, 128), 1)
    except:
        continue
'''
直线提取
'''
rho = 1
theta = np.pi / 180
threshold = 170
minlinelength = 500
maxlinegap = 150
lines = cv2.HoughLinesP(edges, rho, theta, threshold, minLineLength=minlinelength, maxLineGap=maxlinegap)
chs_cp = chs_src.copy()
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(chs_cp, (x1, y1), (x2, y2), (0, 0, 128), 1)
cv2.namedWindow('lines',0)
cv2.resizeWindow('lines', width,height)
cv2.imshow('lines', chs_cp)


'''
点提取
'''
corners = []
img_cp = chs_src.copy()
functions.detect_cross_point(chs_src.shape[1], chs_src.shape[0],lines,0.4,corners)
for corner in corners:
    cv2.circle(img_cp, corner, 1, (0, 255, 0), 4)
cv2.namedWindow('corners', 0)
cv2.resizeWindow('corners',width,height)
cv2.namedWindow('lines', cv2.WINDOW_AUTOSIZE)
cv2.imshow('corners', img_cp)
cv2.waitKey()
cv2.destroyAllWindows()
'''
点分类
'''
# img_cp = chs_src.copy()
# classified_corners = functions.extract_corner(corners, 3)
# print(len(classified_corners))
# for corner in classified_corners:
#     cv2.circle(img_cp, corner, 1, (0, 255, 0), 4)
# cv2.namedWindow('corners_s', 0)
# cv2.resizeWindow('corners_s',width,height)
# cv2.namedWindow('lines', cv2.WINDOW_AUTOSIZE)
# cv2.imshow('corners_s', img_cp)

a = functions.chessboard_distance_cal(corners,70,170)
print(a)

# cv2.namedWindow('edges',cv2.WINDOW_AUTOSIZE)
# cv2.resizeWindow('edge',1600, int(1600*ratio))
# cv2.imshow('edges', edges)

