import cv2
import functions
import numpy as np





# mean = 150
path = '.\\target\\10.bmp'
print(path)
tri_src = cv2.imread(path)
tri_src = cv2.GaussianBlur(tri_src,(7,7),20)
# cv2.namedWindow('src',0)
# cv2.resizeWindow('src',1500,1000)
# cv2.imshow('src',tri_src)
# cv2.waitKey()
gray = cv2.cvtColor(tri_src, cv2.COLOR_BGR2GRAY)
size = gray.shape
print(size)
# tri_auto, src_mean = functions.auto_exposure(gray, mean,True)
# cv2.namedWindow('auto',0)
# cv2.resizeWindow('auto',1500,1000)
# cv2.imshow('auto', tri_auto)
# threshold = (src_mean - 150) * (170/ 50) + 25
# print(threshold)
# ratio = tri_src.shape[0] / tri_src.shape[1]
'''
自动曝光调试
'''
# cv2.namedWindow('thresh_test',0)
# cv2.resizeWindow('thresh_test',900,600)
#
# def update(x):
#     pass
#
#
# cv2.createTrackbar('upper', 'thresh_test', 0, 255, update)
# cv2.createTrackbar('lower', 'thresh_test', 0, 255, update)
# cv2.setTrackbarPos('upper','thresh_test', 255)
# cv2.setTrackbarPos('lower','thresh_test', 67)
#
# while (1):
#     upper = cv2.getTrackbarPos('upper', 'thresh_test')
#     lower = cv2.getTrackbarPos('lower', 'thresh_test')
#     ret, img = cv2.threshold(gray, lower, upper, cv2.THRESH_BINARY)
#     cv2.imshow('thresh_test', img)
#     k = cv2.waitKey(1)
#     if k == ord('e'):
#         up = upper
#         low = lower
#         print('thresh:', up, low)
#         cv2.destroyAllWindows()
#         break

'''
阈值处理
'''
low = 50
up = 255
ret, thresh_img = cv2.threshold(gray, low, up, cv2.THRESH_BINARY_INV)
# cv2.namedWindow('thresh_img', 0)
# cv2.resizeWindow('thresh_img', 1500, 1000)
# cv2.imshow('thresh_img', thresh_img)
# cv2.waitKey()
# cv2.destroyAllWindows()

# functions.find_tri_corner(thresh_img)

'''
边缘检测调试
'''
# cv2.namedWindow('canny_test', 0)
# cv2.resizeWindow('canny_test', 1700,1200)
#
#
# def update(x):
#     pass
#
#
# cv2.createTrackbar('upper', 'canny_test', 1, 255, update)
# cv2.createTrackbar('lower', 'canny_test', 1, 255, update)
# cv2.setTrackbarPos('upper','canny_test',50)
# cv2.setTrackbarPos('lower','canny_test',160)
#
# while (1):
#     cp = thresh_img.copy()
#     upper = cv2.getTrackbarPos('upper', 'canny_test')
#     lower = cv2.getTrackbarPos('lower', 'canny_test')
#     edges = cv2.Canny(gray, lower, upper)
#     cv2.imshow('canny_test', edges)
#     k = cv2.waitKey(1)
#     if k == ord('e'):
#         up = upper
#         low = lower
#         print('edge:', up, low)
#         cv2.destroyAllWindows()
#         break

'''
边缘提取
'''
low = 50
up = 160
edges = cv2.Canny(gray, low, up)
# cv2.namedWindow('edges',0)
# cv2.resizeWindow('edges', 1500,1000)
# cv2.imshow('edges',edges)

'''
contours
'''
result = np.zeros(size, dtype = np.uint8)
out_binary, contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for cnt in range(len(contours)):
    cv2.drawContours(result, contours, cnt, 255, 1)
cv2.namedWindow('cnt',0)
cv2.resizeWindow('cnt', 900, 600)
cv2.imshow('cnt', result)
cv2.waitKey()
cv2.destroyAllWindows()

'''
霍夫直线调试
'''


# def nothing(x):
#     pass
#
#
# masked_src_lines = edges.copy()
# cv2.namedWindow('test', 0)
# cv2.resizeWindow('test', 1500, 1200)
# cv2.createTrackbar('angle_resolution', 'test', 1, 720, nothing)
# cv2.createTrackbar('rho', 'test', 1, 100, nothing)
# cv2.createTrackbar('threshold', 'test', 1, 200, nothing)
# cv2.createTrackbar('minlinelength', 'test', 1, 500, nothing)
# cv2.createTrackbar('minlinegap', 'test', 1, 500, nothing)
# cv2.setTrackbarPos('rho', 'test', 50)
# cv2.setTrackbarPos('angle_resolution', 'test', 360)
# cv2.setTrackbarPos('threshold', 'test', 140)
# cv2.setTrackbarPos('minlinelength', 'test', 500)
# cv2.setTrackbarPos('minlinegap', 'test', 150)
# while (1):
#     cv2.imshow('test', masked_src_lines)
#     masked_src_lines = tri_src.copy()
#     angle_resolution = int(cv2.getTrackbarPos('angle_resolution', 'test'))
#     theta = np.pi / angle_resolution
#     rho = cv2.getTrackbarPos('rho', 'test') / 50
#     threshold = int(cv2.getTrackbarPos('threshold', 'test'))
#     minlinelength = int(cv2.getTrackbarPos('minlinelength', 'test'))
#     minlinegap = int(cv2.getTrackbarPos('minlinegap', 'test'))
#     lines = cv2.HoughLinesP(result, rho, theta, threshold, minLineLength=minlinelength, maxLineGap=minlinegap)
#     try:
#         for line in lines:
#             x1, y1, x2, y2 = line[0]
#             cv2.line(masked_src_lines, (x1, y1), (x2, y2), (0, 128, 0), 5)
#     except:
#         continue
#     k = cv2.waitKey(1)
#     if k == ord('e'):
#         angle = angle_resolution
#         t = theta
#         rho = rho
#         ths = threshold
#         min = minlinelength
#         max = minlinegap
#         print('angle:',angle, ' theta:', t, ' rho:', rho,' threshold:', ths, ' minlinelength:', min, ' maxlinegap:', max)
#         break
'''
霍夫直线提取
'''
rho = 1
angle = 360
ths = 140
min = 500
max = 150

lines = cv2.HoughLinesP(result,rho,np.pi/angle,ths, minLineLength = min,maxLineGap=max)

points= []
functions.detect_cross_point(size[1],size[0],lines,100000,points)
corners = functions.extract_triangle_corner(points,20)
corners = functions.find_perpen_corner(corners[0],corners[1],corners[2])
corners = [corners['foot'],corners['corner1'],corners['corner2']]
for corner in corners:
    cv2.circle(tri_src, corner, 1, (0, 0, 255), 20)
# cv2.namedWindow('corners',0)
# cv2.resizeWindow('corners',900,600)
# cv2.imshow('corners',tri_src)
# cv2.waitKey()
# cv2.destroyAllWindows()
print(corners)
'''
直线提取
'''
# rho = 1
# theta = np.pi / 360
# threshold = 140
# minlinelength = 500
# maxlinegap = 150
# lines = cv2.HoughLinesP(edges, rho, theta, threshold, minLineLength=minlinelength, maxLineGap=maxlinegap)
# tri_cp = tri_src.copy()
# for line in lines:
#     x1, y1, x2, y2 = line[0]
#     cv2.line(tri_cp, (x1, y1), (x2, y2), (0, 0, 128), 1)
# print(len(lines))
# cv2.namedWindow('lines', 0)
# cv2.resizeWindow('lines', 1500, 1000)
# cv2.imshow('lines', tri_cp)
#
# '''
# 点提取
# '''
# corners = []
# img_cp = tri_src.copy()
# functions.detect_cross_point(tri_src.shape[1], tri_src.shape[0],lines,200,corners)
# for corner in corners:
#     cv2.circle(img_cp, corner, 1, (0, 255, 0), 4)
# cv2.namedWindow('corners', 0)
# cv2.resizeWindow('corners',1500,1000)
# cv2.namedWindow('lines', cv2.WINDOW_AUTOSIZE)
# cv2.imshow('corners', img_cp)

# classified_corners = functions.extract_corner(corners,5)
# print(len(classified_corners))
# img_cp = tri_src.copy()
# for corner in classified_corners:
#     cv2.circle(img_cp, corner, 1, (0, 255, 0), 4)
# cv2.namedWindow('corners', 0)
# cv2.resizeWindow('corners',1500,1000)
# cv2.namedWindow('lines', cv2.WINDOW_AUTOSIZE)
# cv2.imshow('corners', img_cp)
'''
霍夫圆调试
'''

def nothing(x):
    pass

cv2.namedWindow('circle_test', 0)
cv2.resizeWindow('circle_test', 1700,1200)
cv2.createTrackbar('num1','circle_test',1,400,nothing)
cv2.createTrackbar('num2','circle_test',1,400,nothing)
cv2.createTrackbar('param1','circle_test',1,400,nothing)
cv2.createTrackbar('param2','circle_test',1,400,nothing)
cv2.createTrackbar('minradius','circle_test',1,400,nothing)
cv2.createTrackbar('maxradius','circle_test',1,400,nothing)
cv2.setTrackbarPos('num1','circle_test',1)
cv2.setTrackbarPos('num2','circle_test',80)
cv2.setTrackbarPos('param1','circle_test',160)
cv2.setTrackbarPos('param2','circle_test',30)
cv2.setTrackbarPos('minradius','circle_test',150)
cv2.setTrackbarPos('maxradius','circle_test',350)
while (1):
    k = cv2.waitKey(1)
    if k == ord('e'):
        break
    masked_src_lines = thresh_img.copy()
    num1 =  cv2.getTrackbarPos('num1','circle_test')
    num2 = cv2.getTrackbarPos('num2', 'circle_test')
    param1 = cv2.getTrackbarPos('param1', 'circle_test')
    param2 = cv2.getTrackbarPos('param2', 'circle_test')
    minradius = cv2.getTrackbarPos('minradius', 'circle_test')
    maxradius = cv2.getTrackbarPos('maxradius', 'circle_test')

    circle1 = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp = num1, minDist = num2, param1=param1, param2=param2, minRadius=minradius,
                               maxRadius=maxradius)  # 把半径范围缩小点，检测内圆，瞳孔
    # if len(circle1)==0:
    #     cv2.imshow('circle_test', tri_cp)
    #     continue
    # else:
    try:
        circles = np.uint16(np.around(circle1))
        tri_cp = tri_src.copy()
        for i in circles[0,:]:
            cv2.circle(tri_cp, (i[0], i[1]), i[2], (255, 0, 0), 5)  # 画圆
            cv2.circle(tri_cp, (i[0], i[1]), 2, (0,255,0), 10)  # 画圆心
        cv2.imshow('circle_test', tri_cp)
    except:
        raise Exception('nothing')



circle1 = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp = 1,minDist = 80, param1=160, param2=30, minRadius=150, maxRadius=350)  #把半径范围缩小点，检测内圆，瞳孔
circles = np.uint16(np.around(circle1))
for i in circles[0,:]:
    cv2.circle(tri_src, (i[0], i[1]), i[2], (255, 0, 0), 5)  # 画圆
    cv2.circle(tri_src, (i[0], i[1]), 2, (0,255,0), 10)  # 画圆心
    print('center:', (i[0],i[1]), 'radius ', i[2])
cv2.namedWindow('circles',0)
cv2.resizeWindow('circles',1500,1000)
cv2.imshow('circles', tri_src)
cv2.waitKey()
cv2.destroyAllWindows()


# cv2.namedWindow('edges',cv2.WINDOW_AUTOSIZE)
# cv2.resizeWindow('edge',1600, int(1600*ratio))
# cv2.imshow('edges', edges)
