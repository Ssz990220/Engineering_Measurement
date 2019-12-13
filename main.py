import cv2
import numpy as np
import functions

k_threshold = 0.1
angle_resolution_factor = 180
src = cv2.imread('.\chessboard\\20191108115311248.bmp')
chessboard_template = cv2.imread('chessboard_template.jpg')
tl, br = functions.templatematch(src, chessboard_template)
masked_src = functions.generate_mask_img(tl, br, src)

src_gray, src_thresh, src_edges = functions.pre_process(masked_src)

# img_cp = masked_src.copy()
# img_cp_lines = masked_src.copy()
# lines = cv2.HoughLinesP(src_edges, 0.5, np.pi / angle_resolution_factor, 50, minLineLength=100, maxLineGap=100)
# for line in lines:
#     x1, y1, x2, y2 = line[0]
#     cv2.line(img_cp_lines, (x1, y1), (x2, y2), (0, 0, 128), 1)
#
# corners = []
# x_size = masked_src.shape[1]
# y_size = masked_src.shape[0]
# functions.detect_cross_point(x_size, y_size, lines, k_threshold, corners)
# for corner in corners:
#     cv2.circle(img_cp, corner, 1, (0, 255, 0), 4)
# cv2.namedWindow('corners', cv2.WINDOW_AUTOSIZE)
# cv2.namedWindow('lines', cv2.WINDOW_AUTOSIZE)
# cv2.imshow('corners', img_cp)
# cv2.imshow('lines',img_cp_lines)
# cv2.waitKey()
# cv2.destroyAllWindows()


def nothing(x):
    pass
masked_src_lines = masked_src.copy()
cv2.namedWindow('test',cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar('angle_resolution','test',1, 720,nothing)
cv2.createTrackbar('rho','test',1,100,nothing)
cv2.createTrackbar('threshold','test',1,200,nothing)
cv2.createTrackbar('minlinelength','test',1,500,nothing)
cv2.createTrackbar('minlinegap','test',1,500,nothing)

while(1):
    cv2.imshow('test',masked_src_lines)
    masked_src_lines = masked_src.copy()
    k = cv2.waitKey(1)&0xFF
    if k == 27:
        break
    angle_resolution = int(cv2.getTrackbarPos('angle_resolution','test'))
    theta = np.pi/angle_resolution
    rho = cv2.getTrackbarPos('rho','test')/50
    threshold = int(cv2.getTrackbarPos('threshold','test'))
    minlinelength = int(cv2.getTrackbarPos('minlinelength','test'))
    minlinegap = int(cv2.getTrackbarPos('minlinegap','test'))
    lines = cv2.HoughLinesP(src_edges,rho, theta, threshold, minLineLength = minlinelength, maxLineGap = minlinegap)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(masked_src_lines, (x1, y1), (x2, y2), (0, 0, 128), 1)

cv2.destroyAllWindows()