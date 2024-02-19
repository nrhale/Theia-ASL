import cv2
from price_testing.HandTrackingModule import HandDetector
#from cvzone.HandTrackingModule import HandDetector #old version
from cvzone.ClassificationModule import Classifier
import numpy as np
import math

#0 is id number of webcam
#Note: make sure camera access is enabled
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1) # may change later
classifier = Classifier("model_c_18/keras_model.h5", "model_c_18/labels.txt")

imgSize= 300
# create offset for crop size
offset = 20

folder = "custom_images/C"
counter = 0

labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y"]
# j missing above (dynamic)

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0] # because we just have the one hand
        x,y,w,h = hand['bbox'] #gets us all the values

        #making all images the same size

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8)*255 #imgSize x imgSize square
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
            prediction,index = classifier.getPrediction(imgWhite)
            letter_seen = labels[index]
            print(f"Detected letter: {letter_seen}")
            print(prediction, index)
           # print(index)

        else:
            k = imgSize/w
            hCal = math.ceil(k*h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize-hCal)/2)
            try:
                imgWhite[hGap:hCal+hGap, :] = imgResize
                print("yo")
                prediction, index = classifier.getPrediction(imgWhite)
                letter_seen = labels[index]
                print(f"Detected letter: {letter_seen}")
                print(prediction, index)
            except:
                print("get back in range")








        cv2.imshow("ImageCrop", imgCrop)
        cv2.imshow("ImageOverlay", imgWhite)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

