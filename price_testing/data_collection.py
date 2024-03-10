import cv2
from price_testing.HandTrackingModule import HandDetector
import numpy as np
import math
import time

#0 is id number of webcam
#Note: make sure camera access is enabled
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1) # may change later

imgSize= 300
# create offset for crop size
offset = 20

folder = "custom_images/2i"
counter = 0

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    #hands, img = detector.mp_findHands(img)
    #result = hands.process(img)
    #hand_la
    #detector.
    if hands:
        hand = hands[0] # because we just have the one hand
        x,y,w,h = hand['bbox'] #gets us all the values
        #cv2.imshow("hand", hands[0])
        #detector.results = detector.hands.process(img)

        #making all images the same size

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8)*255 #imgSize x imgSize square
        #cv2.cvtColor(imgWhite, cv2.COLOR_BGR2RGB)
        #np.uint8 restricts it to 8 bits (0 to 255)
        imgCrop = img[y-offset:y+h+offset, x-offset:x+w+offset] #starting height, ending height, starting width, ending width

        imgCropShape = imgCrop.shape
        #imgWhite[0:imgCropShape[0], 0:imgCropShape[1]] = imgCrop

        aspectRatio = h/w

        if aspectRatio > 1:
            k = imgSize/h
            wCal = math.ceil(k*w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize-wCal)/2)
            imgWhite[:, wGap:wCal+wGap] = imgResize

        else:
            k = imgSize/w
            hCal = math.ceil(k*h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize-hCal)/2)
            try:
                imgWhite[hGap:hCal+hGap, :] = imgResize
            except:
                print("get back in range")







        cv2.imshow("ImageCrop", imgCrop)
        cv2.imshow("ImageWhite", imgWhite)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord("s") and counter < 1200:
        counter += 1
        cv2.imwrite(f'{folder}/Image_{time.time()}.jpg', imgWhite)
        print(counter)