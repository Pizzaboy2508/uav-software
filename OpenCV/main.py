import cv2 as cv
import numpy as np

from PIL import Image
from util import get_limits

#color in BGR colorspace
bgrColor = [0, 255, 255]
#id of first webcam on system is 0 by default, might need to change for Pi camera  
cap = cv.VideoCapture(0)

# Counter to track saved frames
saved_frames = 0
max_frames = 5

while True:
    ret, frame = cap.read()

    #convert BGR (RGB) to HSV colour space
    hsvImage = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    #from util, converts the BGR colour to the HSV colour spectrum
    lowerLimit, upperLimit = get_limits(color=bgrColor)

    #returns a location (mask) of all the desired pixels within the frame 
    mask = cv.inRange(hsvImage, lowerLimit, upperLimit)

    mask_ = Image.fromarray(mask)

    bbox = mask_.getbbox()

    #creates red border around found color
    if bbox is not None:
        x1, y1, x2, y2 = bbox

        frame = cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 5)

        if saved_frames < max_frames:
            filename = f'Photos/c{saved_frames + 1}.png'
            cv.imwrite(filename, frame)
            saved_frames +=1
            print(f"Saved frame {saved_frames}: {filename}")

    #window named 'frame'
    cv.imshow('testFrame', frame)

    #window closes when 'q' key is pressed
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()