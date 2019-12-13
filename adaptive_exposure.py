import cv2
import numpy as np
import os

for _,_,files in os.walk('.\\target'):
    file_list = files
for file_name in file_list:
    target_name=('.\\target\\'+file_name)
    img = cv2.imread(target_name)
    array =  np.array(img)
    mean = np.mean(array)
    print(target_name + ': '+str(mean))
