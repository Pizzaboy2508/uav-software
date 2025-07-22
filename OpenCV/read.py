import cv2 as cv
print(cv.__version__)

# takes path of image and returns as matrix of pixels
# use absloute paths
img = cv.imread('Photos/redballoon.jpg')

cv.imshow('Red Balloon', img)

cv.waitKey(0)

#cv.imshow('')