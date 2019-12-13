import cv2
import functions
import numpy as np
import copy

def find_triangle(path, ratio):
    tri_src = cv2.imread(path)
    tri_src = cv2.GaussianBlur(tri_src, (7, 7), 20)
    gray = cv2.cvtColor(tri_src, cv2.COLOR_BGR2GRAY)
    size = gray.shape
    '''
    阈值处理
    '''
    ret, thresh_img = cv2.threshold(gray, 67, 255, cv2.THRESH_BINARY_INV)
    '''
    边缘提取
    '''
    edges = cv2.Canny(gray, 50, 160)

    '''
    find_contour
    '''
    result = np.zeros(size, dtype=np.uint8)
    out_binary, contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in range(len(contours)):
        cv2.drawContours(result, contours, cnt, 255, 1)

    '''
    霍夫直线变换
    '''
    lines = cv2.HoughLinesP(result,1,np.pi/360,140, minLineLength = 500,maxLineGap=150)
    points= []
    functions.detect_cross_point(size[1],size[0],lines,200,points)
    corners = functions.extract_triangle_corner(points,20)
    corners = functions.find_perpen_corner(corners[0],corners[1],corners[2])
    corner = copy.deepcopy(corners)
    corners = [corners['foot'], corners['corner1'], corners['corner2']]

    img = tri_src.copy()
    cv2.circle(img,corner['foot'],2, (0,0,255),10)
    cv2.circle(img,corner['corner1'],2, (0,255,0),5)
    cv2.circle(img,corner['corner2'], 2, (0, 255,0), 10)
    cv2.namedWindow('corners',0)
    cv2.resizeWindow('corners', 900, 600)
    cv2.imshow('corners',img)
    cv2.waitKey()
    cv2.destroyAllWindows()


    '''
    霍夫圆变换
    '''
    circle1 = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp = 1,minDist = 80, param1=160, param2=30, minRadius=150, maxRadius=350)
    circles = np.uint16(np.around(circle1))
    center = (circles[0, 0, 0], circles[0, 0, 1])
    radius = circles[0, 0, 2]
    if len(circles[0, :]) > 1:
        raise Exception('Multiple circles, please adjust the exposure.')
    if len(circles[0,:])<1:
        raise Exception('No circle detected')

    a, b, e, f, alpha = functions.post_process(corners, center)
    d = 2 * radius
    a = a * ratio
    b = b * ratio
    f = f * ratio
    e = e * ratio
    d = d * ratio
    print(
        'a is %5f,\t\t\tb is %5f,\t\t\t\te is %5f,\t\t\tf is %5f,\t\t\td is %5f,\t\t\t\talpha is %5f degree' % (
        a, b, e, f, d, alpha))
    print(
        'a should be 15, \t\tb should be 20,\t\t\t\te should be 5,\t\t\tf should be 5,\t\t\td should be 6,\t\t\t\talpha should be 90')
    print(
        'error of a is %5f,\terror of b is %5f,\terror of e is %5f,\terror of f is %5f,\terror of d is %5f,\terror of alpha is %5f'
        % ((15 - a), (20 - b), (5 - e), (5 - f), 6 - d, 90 - alpha))

    return {'a': a, 'b': b, 'f': f, 'e': e, 'd': d, 'alpha': alpha}


if __name__ == '__main__':
    find_triangle('.\\target\\7.bmp', 0.013778638318145237)
