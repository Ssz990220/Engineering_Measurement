import cv2
import numpy as np
import math


def find_tri_corner(thresh_img, src):
    out_binary, contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    h, w = thresh_img.shape
    result = np.zeros((h, w, 3), dtype=np.uint8)
    for cnt in range(len(contours)):
        epsilon = 0.01 * cv2.arcLength(contours[cnt], True)
        approx = cv2.approxPolyDP(contours[cnt], epsilon, True)
        corners = len(approx)
        if corners == 3:
            area = cv2.contourArea(contours[cnt])
            if area < 10:
                continue
            p = 0
            shape_type = 'triangle'
            print(" 面积: %.3f " % area)
        cv2.drawContours(result, contours, cnt, (0, 255, 0), 1)
    cv2.namedWindow('result',0)
    cv2.resizeWindow('result',900,600)
    cv2.imshow('result',result)
    result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    lines = cv2.HoughLinesP(result, 0.5, np.pi / 360, 140, minLineLength=500, maxLineGap=150)
    points = []
    detect_cross_point(w, h, lines, 200, points)
    src_cp = src.copy()
    tri_corners = extract_triangle_corner(points, 30)
    for point in tri_corners:
        cv2.circle(src_cp, point, 1, (0, 0, 255), 10)
    cv2.namedWindow('src', 0)
    cv2.resizeWindow('src', 1500, 1000)
    cv2.imshow('src', src_cp)
    cv2.waitKey()
    cv2.destroyAllWindows()
    return tri_corners


def find_perpen_corner(point1, point2, point3):
    thresh_perpen = 0.2
    if (point1[0] - point2[0]) == 0:
        k13 = (point1[1] - point3[1]) / (point1[0] - point3[0])
        k23 = (point2[1] - point3[1]) / (point2[0] - point3[0])
        if abs(k13 < thresh_perpen):
            return {'foot': point1, 'corner1': point2, 'corner2': point3}
        elif abs(k23 < thresh_perpen):
            return {'foot': point2, 'corner1': point1, 'corner2': point3}
        else:
            return {'foot': point3, 'corner1': point2, 'corner2': point1}
    if (point1[0] - point3[0]) == 0:
        k12 = (point1[1] - point2[1]) / (point1[0] - point2[0])
        k23 = (point2[1] - point3[1]) / (point2[0] - point3[0])
        if abs(k12) < thresh_perpen:
            return {'foot': point1, 'corner1': point2, 'corner2': point3}
        elif abs(k23) < thresh_perpen:
            return {'foot': point3, 'corner1': point2, 'corner2': point1}
        else:
            return {'foot': point2, 'corner1': point1, 'corner2': point3}
    if (point2[0] - point3[0]) == 0:
        k12 = (point1[1] - point2[1]) / (point1[0] - point2[0])
        k13 = (point1[1] - point3[1]) / (point1[0] - point3[0])
        if abs(k12) < thresh_perpen:
            return {'foot': point2, 'corner1': point1, 'corner2': point3}
        elif abs(k13) < thresh_perpen:
            return {'foot': point3, 'corner1': point2, 'corner2': point1}
        else:
            return {'foot': point1, 'corner1': point2, 'corner2': point3}
    k12 = (point1[1] - point2[1]) / (point1[0] - point2[0])
    k13 = (point1[1] - point3[1]) / (point1[0] - point3[0])
    k23 = (point2[1] - point3[1]) / (point2[0] - point3[0])
    if abs(k12 * k13 + 1) < thresh_perpen:
        return {'foot': point1, 'corner1': point2, 'corner2': point3}
    elif abs(k12 * k23 + 1) < thresh_perpen:
        return {'foot': point2, 'corner1': point1, 'corner2': point3}
    elif abs(k23 * k13 + 1) < thresh_perpen:
        return {'foot': point3, 'corner1': point2, 'corner2': point1}
    else:
        raise Exception("Invalid Corners!")


def generate_mask_img(tl, br, src):
    return src[tl[1]:br[1], tl[0]:br[0]]


def auto_exposure(src, mean, tri):
    if tri == True:
        src_mean = np.mean(src) * 1.5
    else:
        src_mean = np.mean(src)
    print(np.mean(src))
    auto_img = np.uint8(np.clip((src - (src_mean - mean)), 0, 255))
    return auto_img, src_mean


def pre_process(src):
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(src, (5, 5), cv2.BORDER_DEFAULT)
    thresh = 200
    ret, thresh_img = cv2.threshold(blur, thresh, 255, cv2.THRESH_BINARY)
    edges = cv2.Canny(thresh_img, 150, 200)
    return gray, thresh_img, edges


def templatematch(src, template):
    tpl = template
    target = src
    methods = cv2.TM_CCOEFF_NORMED  # ,cv2.TM_CCORR_NORMED,cv2.TM_CCOEFF_NORMED, cv2.TM_SQDIFF_NORMED
    th, tw = tpl.shape[:2]
    result = cv2.matchTemplate(target, tpl, methods)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if methods == cv2.TM_SQDIFF_NORMED:
        tl = min_loc  # tl是左上角点
    else:
        tl = max_loc
    br = (tl[0] + tw, tl[1] + th)  # 右下点
    cv2.rectangle(target, tl, br, (0, 0, 255), 2)
    # cv2.imshow("match-%s" % methods, target)

    return tl, br


def detect_cross_point(x_size, y_size, lines, k_threshold, corners):
    lower_threshold = 0.1
    for i in range(0, len(lines)):
        x11, y11, x12, y12 = lines[i][0]
        if x11 < 5 or y11 < 5 or x12 < 5 or y12 < 5 \
                or x_size - x11 < 5 or y_size - y11 < 5 or x_size - x12 < 5 or y_size - y12 < 5:
            continue
        if x11 == x12:
            horizontal1 = True
        else:
            k1 = (y11 - y12) / (x11 - x12)
            horizontal1 = False
        for j in range(i + 1, len(lines)):
            x21, y21, x22, y22 = lines[j][0]
            if x21 < 5 or y21 < 5 or x22 < 5 or y22 < 5 \
                    or x_size - x21 < 5 or y_size - y21 < 5 or x_size - x22 < 5 or y_size - y22 < 5:
                continue
            if x21 == x22:
                horizontal2 = True
            else:
                k2 = (y21 - y22) / (x21 - x22)
                horizontal2 = False
            if horizontal1:
                if horizontal2:
                    continue
                elif (-k_threshold < k2) and (k2 < k_threshold):
                    cross_x = x11
                    cross_y = y21 + k2 * (x11 - x21)
                else:
                    continue
            else:
                if horizontal2:
                    if (-k_threshold < k1) and (k1 < k_threshold):
                        cross_x = x21
                        cross_y = y11 + k1 * (x21 - x11)
                    else:
                        continue
                else:
                    if abs(k1 - k2) < lower_threshold:
                        continue

                    elif (-1 - k_threshold < k1 * k2) and (k1 * k2 < -1 + k_threshold):
                        cross_x = (y21 - y11 + k1 * x11 - k2 * x21) / (k1 - k2)
                        cross_y = (k1 * k2 * (x21 - x11) + k2 * y11 - k1 * y21) / (k2 - k1)
                    else:
                        continue
            if cross_x > x_size or cross_x < 0:
                continue
            else:
                cross_x = int(cross_x)
            if cross_y > y_size or cross_y < 0:
                continue
            else:
                cross_y = int(cross_y)
            corners.append((cross_x, cross_y))
    return corners


def extract_triangle_corner(points, threshold):
    point1 = (0, 0)
    point1_init = False
    point2 = (0, 0)
    point2_init = False
    point3 = (0, 0)
    point3_init = False
    for point in points:
        if not point1_init:
            point1 = point
            point1_init = True
            continue
        elif distance(point1, point) < threshold:
            point1 = ((point1[0] + point[0]) / 2, (point1[1] + point[1]) / 2)
            continue
        elif not point2_init:
            point2 = point
            point2_init = True
            continue
        elif distance(point2, point) < threshold:
            point2 = ((point2[0] + point[0]) / 2, (point2[1] + point[1]) / 2)
            continue
        elif not point3_init:
            point3 = point
        elif distance(point3, point) < threshold:
            point3 = ((point3[0] + point[0]) / 2, (point3[1] + point[1]) / 2)
            continue
    point1 = (int(point1[0]), int(point1[1]))
    point2 = (int(point2[0]), int(point2[1]))
    point3 = (int(point3[0]), int(point3[1]))
    if point1[0] == 0 & point1[1] == 0  & point2[0]==0 & point2[1]==0:
        raise Exception ("not enough points detected, please adjust the exposure")
    return [point1, point2, point3]


def distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5


def chessboard_distance_cal(points, lower_threshold, upper_threshold):
    counter = 0
    distance = 0
    for i in range(0, len(points)):
        for j in range(i + 1, len(points)):
            if abs(points[i][0] - points[j][0]) > upper_threshold or abs(points[i][1] - points[j][1]) > upper_threshold:
                continue
            elif (points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2 < lower_threshold ** 2:
                continue
            elif (points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2 > upper_threshold ** 2:
                continue
            else:
                distance += ((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2) ** 0.5
                counter += 1
    return distance / counter


def vector_cross(vector1, vector2):
    return abs(vector1[0] * vector2[1] - vector1[1] * vector2[0])


def post_process(corners, center):
    foot_check = find_perpen_corner(corners[0], corners[1], corners[2])
    vector_1f = (foot_check['foot'][0] - foot_check['corner1'][0], foot_check['foot'][1] - foot_check['corner1'][1])
    vector_2f = (foot_check['foot'][0] - foot_check['corner2'][0], foot_check['foot'][1] - foot_check['corner2'][1])
    vector_cf = (foot_check['foot'][0] - center[0], foot_check['foot'][1] - center[1])
    vector_c1 = (foot_check['corner1'][0] - center[0], foot_check['corner1'][1] - center[1])
    vector_c2 = (foot_check['corner2'][0] - center[0], foot_check['corner2'][1] - center[1])
    length1 = distance(foot_check['foot'], foot_check['corner1'])
    length2 = distance(foot_check['foot'], foot_check['corner2'])
    h1 = vector_cross(vector_c1, vector_cf) / length1
    h2 = vector_cross(vector_c2, vector_cf) / length2
    h = vector_cross(vector_1f, vector_2f) / length2
    alpha = math.asin(h / length1) / np.pi * 180
    if length1 > length2:
        b = length1
        a = length2
        e = h1
        f = h2
    else:
        b = length2
        a = length1
        e = h2
        f = h1
    return a, b, e, f, alpha
