import cv2
import numpy as np

im = cv2.imread('res/WoWScrnShot_082720_020112.jpg')

h, w, c = im.shape
im = im[int(h * 0.35): int(h * 0.65), int(w * 0.45): int(w * 0.55), :]
im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

maxima = np.argmax(im, axis=1)
mask = np.copy(im) * 0

for i, j in enumerate(maxima):
    mask[i, j] = 255

rho = 1
theta = np.pi / 180
threshold = 15
min_line_length = 50
max_line_gap = 4
line_image = np.copy(mask) * 0

lines = cv2.HoughLinesP(mask, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

for line in lines:
    for x1, y1, x2, y2 in line:
        cv2.line(mask, (x1, y1), (x2, y2), (255, 0, 0), 5)

cv2.imshow('b', mask)
cv2.imshow('a', im)
cv2.waitKey(0)
