import cv2 as cv
import numpy as np


class ShapeAnalysis:
    def __init__(self):
        self.shapes = {'triangle': 0, 'rectangle': 0, 'polygons': 0, 'circles': 0}

    def analysis(self, frame):
        h, w, ch = frame.shape
        result = np.zeros((h, w, ch), dtype=np.uint8)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # cv.namedWindow('thresh_test', cv.WINDOW_NORMAL)
        # cv.resizeWindow('thresh_test', 1500, 1000)
        #
        # def update(x):
        #     pass
        #
        # cv.createTrackbar('lower', 'thresh_test', 0, 255, update)
        #
        # while (1):
        #     k = cv.waitKey(1)
        #     if k == ord('e'):
        #         break
        #     lower = cv.getTrackbarPos('lower', 'thresh_test')
        #     ret, img = cv.threshold(gray, lower, 255, cv.THRESH_BINARY_INV)
        #     out_binary, contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        #     for cnt in range(len(contours)):
        #         # 提取与绘制轮廓
        #         cv.drawContours(result, contours, cnt, (0, 255, 0), 1)
        #         # 轮廓逼近
        #     cv.imshow('thresh_test', result)

        ret, binary = cv.threshold(gray, 50, 255, cv.THRESH_BINARY_INV)
        # cv.imshow("input image", binary)

        out_binary, contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        # print(np.shape(contours))

        for cnt in range(len(contours)):
            # 提取与绘制轮廓
            cv.drawContours(result, contours, cnt, (0, 255, 0), 1)
            # 轮廓逼近
        #     epsilon = 0.01 * cv.arcLength(contours[cnt], True)
        #     approx = cv.approxPolyDP(contours[cnt], epsilon, True)
        #
        #     # 分析几何形状
        #     corners = len(approx)
        #     shape_type = ""
        #     if corners == 3:
        #         count = self.shapes['triangle']
        #         count = count + 1
        #         self.shapes['triangle'] = count
        #         shape_type = "三角形"
        #     if corners != 3:
        #         continue
        #     #     count = self.shapes['circles']
        #     #     count = count + 1
        #     #     self.shapes['circles'] = count
        #     #     shape_type = "圆形"
        #
        #     # # 求解中心位置
        #     # mm = cv.moments(contours[cnt])
        #     # cx = int(mm['m10'] / mm['m00'])
        #     # cy = int(mm['m01'] / mm['m00'])
        #     # cv.circle(result, (cx, cy), 3, (0, 0, 255), -1)
        #
        #     # 颜色分析
        #     # color = frame[cy][cx]
        #     # color_str = "(" + str(color[0]) + ", " + str(color[1]) + ", " + str(color[2]) + ")"
        #
        #     # 计算面积与周长
        #     p = cv.arcLength(contours[cnt], True)
        #     area = cv.contourArea(contours[cnt])
        #     print("周长: %.3f, 面积: %.3f 颜色:  形状: %s " % (p, area, shape_type))
        result = cv.cvtColor(result, cv.COLOR_BGR2GRAY)
        def nothing(x):
            pass


        masked_src_lines = result.copy()
        cv.namedWindow('test', 0)
        cv.resizeWindow('test', 1500, 1200)
        cv.createTrackbar('angle_resolution', 'test', 1, 720, nothing)
        cv.createTrackbar('rho', 'test', 1, 100, nothing)
        cv.createTrackbar('threshold', 'test', 1, 200, nothing)
        cv.createTrackbar('minlinelength', 'test', 1, 500, nothing)
        cv.createTrackbar('minlinegap', 'test', 1, 500, nothing)
        cv.setTrackbarPos('rho', 'test', 50)
        cv.setTrackbarPos('angle_resolution', 'test', 360)
        cv.setTrackbarPos('threshold', 'test', 140)
        cv.setTrackbarPos('minlinelength', 'test', 500)
        cv.setTrackbarPos('minlinegap', 'test', 150)
        while (1):
            cv.imshow('test', masked_src_lines)
            masked_src_lines = frame.copy()
            k = cv.waitKey(1) & 0xFF
            if k == 27:
                break
            angle_resolution = int(cv.getTrackbarPos('angle_resolution', 'test'))
            theta = np.pi / angle_resolution
            rho = cv.getTrackbarPos('rho', 'test') / 50
            threshold = int(cv.getTrackbarPos('threshold', 'test'))
            minlinelength = int(cv.getTrackbarPos('minlinelength', 'test'))
            minlinegap = int(cv.getTrackbarPos('minlinegap', 'test'))
            lines = cv.HoughLinesP(result, rho, theta, threshold, minLineLength=minlinelength, maxLineGap=minlinegap)
            print(len(lines))
            try:
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    cv.line(masked_src_lines, (x1, y1), (x2, y2), (0, 128, 0), 2)
            except:
                continue
        cv.namedWindow('Analysis Result', 0)
        cv.resizeWindow('Analysis Result', 1500, 1000)
        cv.imshow("Analysis Result", result)
        # cv.imwrite("D:/test-result.png", self.draw_text_info(result))
        return self.shapes

    # def draw_text_info(self, image):
    #     c1 = self.shapes['triangle']
    #     c4 = self.shapes['circles']
    #     cv.putText(image, "triangle: " + str(c1), (10, 20), cv.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 12)
    #     cv.putText(image, "circles: " + str(c4), (10, 80), cv.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 12)
    #     return image


if __name__ == "__main__":
    src = cv.imread(".\\target\\12.bmp")
    ld = ShapeAnalysis()
    ld.analysis(src)
    cv.waitKey(0)
    cv.destroyAllWindows()
