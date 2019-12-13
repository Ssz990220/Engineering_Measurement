import cv2

def pre_process(src):
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    thresh = 200
    ret, thresh_img = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
    edges = cv2.Canny(thresh_img, 100 ,200)
    return gray, thresh_img, edges