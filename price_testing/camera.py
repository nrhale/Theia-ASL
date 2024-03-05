import cv2
from HandTrackingModule import HandDetector
import numpy as np
import math
import time

#0 is id number of webcam
#Note: make sure camera access is enabled
'''
cap = cv2.VideoCapture(-1)
if not cap.isOpened():
    print("Error: Camera not opened.")
    exit()
detector = HandDetector(maxHands=1) # may change later
'''

imgSize= 300
# create offset for crop size
offset = 20

folder = "custom_images/2y"
counter = 0

while True:
    #success, img = cap.read() ### IMAGE REPLACE
    #hands, img = detector.findHands(img)


    #Set the desired resolution
    width = 1920
    height = 1080

    # Create a green placeholder image
    green_img = np.zeros((height, width, 3), dtype=np.uint8)
    green_img[:, :] = (0, 255, 0)  # Set all pixels to green

    # Set success to True to indicate a successful read
    success = True

    # Assign the green placeholder image to img
    img = green_img


    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord("s") and counter < 1200:
        counter += 1
        cv2.imwrite(f'{folder}/Image_{time.time()}.jpg', imgWhite)
        print(counter)
