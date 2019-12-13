import cv2

chessboard_template = cv2.imread('chessboard.png')
chessboard_gray = cv2.cvtColor(chessboard_template, cv2.COLOR_BGR2GRAY)
cv2.imshow('chessboard', chessboard_gray)

thresh = 200
target = cv2.imread('test.bmp')
target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
ret, target_thresh = cv2.threshold(target_gray, thresh, 255, cv2.THRESH_BINARY)
cv2.imshow("target", target_thresh)
methods = cv2.TM_CCOEFF_NORMED

result = cv2.matchTemplate(target_thresh, chessboard_gray, methods)
th, tw = chessboard_template.shape[:2]
min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(result)
tl = max_loc
br = (tl[0]+tw,tl[1]+th)    #右下点
cv2.rectangle(target,tl,br,(0,0,255),2)
cv2.imshow("match",target)
cv2.waitKey()
cv2.destroyAllWindows()