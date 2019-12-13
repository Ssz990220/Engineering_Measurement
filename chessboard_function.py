import cv2
import functions
import numpy as np


# 曝光范围 180-210

def calibrate_camera(path):
    # mean = 150
    chs_src = cv2.imread(path)
    gray = cv2.cvtColor(chs_src, cv2.COLOR_BGR2GRAY)
    # chs_auto, src_mean = functions.auto_exposure(gray, mean,False)
    # threshold = int((src_mean - 150) * (125 / 70)) - 25
    '''
    阈值处理
    '''

    ret, thresh_img = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    # black_area = sum(sum(thresh_img == 0))  # 通过黑色的面积得知相机到平面的距离
    # upper_thresh = black_area / (thresh_img.shape[0] * thresh_img.shape[1])  ##需要标定

    '''1
    边缘提取
    '''
    edges = cv2.Canny(thresh_img, 150, 200)

    '''
    直线提取
    '''
    rho = 1
    theta = np.pi / 180
    threshold = 170
    minlinelength = 500
    maxlinegap = 150
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, minLineLength=minlinelength, maxLineGap=maxlinegap)

    '''
    点提取
    '''
    corners = []
    functions.detect_cross_point(chs_src.shape[1], chs_src.shape[0], lines, 0.4, corners)
    '''
    点分类
    '''
    #第一个值为lower_threshold 若两点距离小于该值，则认定为同一点
    #显然该算法存在误差，其误差出现在边框上。希望不足以造成过大影响
    a = functions.chessboard_distance_cal(corners, 70, 170)

    return 2/a,a

if __name__ == '__main__':
    print(calibrate_camera('expose.BMP'))

