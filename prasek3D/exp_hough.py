from __future__ import division

import cv2
import numpy as np
import matplotlib.pyplot as plt

from skimage import data, color
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
from skimage.draw import circle_perimeter
from skimage.util import img_as_ubyte


fname = '/home/tomas/Dropbox/Data/Kana/3Dprasek-1_02-1000x2.png'
img = cv2.imread(fname, 0)

# # Load picture and detect edges
# image = img_as_ubyte(img)
# edges = canny(image, sigma=3, low_threshold=10, high_threshold=30)
#
# # Detect two radii
# hough_radii = np.arange(20, 35, 2)
# hough_res = hough_circle(edges, hough_radii)
#
# # Select the most prominent 3 circles
# accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii, total_num_peaks=10)
#
# # Draw them
# fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 4))
# image = color.gray2rgb(image)
# for center_y, center_x, radius in zip(cy, cx, radii):
#     circy, circx = circle_perimeter(center_y, center_x, radius)
#     image[circy, circx] = (220, 20, 20)
#
# ax.imshow(image, cmap=plt.cm.gray)
# plt.show()

# img2 = cv2.medianBlur(img, 5)

# cv2.imshow('smoothing', np.hstack((img, img2)))
# cv2.waitKey(0)

cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20, param1=30, param2=30, minRadius=5, maxRadius=150)
circles = np.uint16(np.around(circles))
for i in circles[0, :100]:
    # draw the outer circle
    cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 1)
    # draw the center of the circle
    cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 1)

cv2.imshow('detected circles', cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()