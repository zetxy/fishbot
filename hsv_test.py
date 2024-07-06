import cv2
import numpy as np

img = cv2.imread('test.png')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_red = np.array([0, 120, 5])
upper_red = np.array([10, 255, 255])

mask0 = cv2.inRange(hsv, lower_red, upper_red)

img[np.where(mask0 == 0)] = 0

cv2.imwrite('uwu.png', img)
