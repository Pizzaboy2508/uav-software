import cv2 as cv
import numpy as np

def get_limits(color):

    c = np.uint8([[color]]) # BGR values
    hsvC = cv.cvtColor(c, cv.COLOR_BGR2HSV) # Coverting to HSV

    hue = hsvC[0][0][0] # Getting hue value

    # for red
    redLower = np.array([136, 87, 111], np.uint8)
    redUpper = np.array([180, 255, 255], np.uint8)
    
    #NEED TO FIX THIS
    # Fixes bug since color red can wrap around hue axis
    if hue >= 165:  # Upper limit for divided red hue
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([180, 255, 255], dtype=np.uint8)
    elif hue <= 15:  # Lower limit for divided red hue
        lowerLimit = np.array([0, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
    else:
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
    
    return lowerLimit, upperLimit