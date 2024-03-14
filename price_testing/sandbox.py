import cv2
from price_testing.HandTrackingModule import HandDetector
#from cvzone.HandTrackingModule import HandDetector #old version
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import keyboard
from price_testing.sign_info import*
from price_testing.common import*

#0 is id number of webcam
#Note: make sure camera access is enabled
def run_sandbox(module):
    labels = create_si_name_list(SI_LIST, module.module_name)

    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=1) # may change later

    classifier = Classifier(f"{module.model}/keras_model.h5", f"{module.model}/labels.txt")

    imgSize= 300
    # create offset for crop size
    offset = 20
    lol = True

    while lol == True:
        success, img = cap.read()
        hands, img = detector.findHands_sandbox(img)
        if hands:
            hand = hands[0] # because we just have the one hand
            x,y,w,h = hand['bbox'] #gets us all the values

            #making all images the same size

            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8)*255 #imgSize x imgSize square
            imgCrop = img[y-offset:y+h+offset, x-offset:x+w+offset] #starting height, ending height, starting width, ending width

            imgCropShape = imgCrop.shape
            aspectRatio = h/w

            if aspectRatio > 1:
                try:
                    k = imgSize/h
                    wCal = math.ceil(k*w)
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                    imgResizeShape = imgResize.shape
                    wGap = math.ceil((imgSize-wCal)/2)
                    imgWhite[:, wGap:wCal+wGap] = imgResize
                    prediction,index = classifier.getPrediction(imgWhite)
                    letter_seen = labels[index]
                    print(f"Detected letter: {letter_seen}")
                    cv2.putText(img, labels[index], (x - 30, y - 30), cv2.FONT_HERSHEY_PLAIN, 6,
                                (0, 0, 0), 2)
                except:
                    print("get back in range")
            else:
                try:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    imgResizeShape = imgResize.shape
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap:hCal+hGap, :] = imgResize
                    prediction, index = classifier.getPrediction(imgWhite)
                    letter_seen = labels[index]
                    print(f"Detected letter: {letter_seen}")
                    cv2.putText(img, labels[index], (x - 30, y - 30), cv2.FONT_HERSHEY_PLAIN, 6,
                                (0, 0, 0), 2)
                except:
                    print("get back in range")

        cv2.imshow(f"SANDBOX: {module.module_name}", img)
        key = cv2.waitKey(1)
        if keyboard.is_pressed('z'):
            lol = False
            cv2.destroyAllWindows()

if __name__ == "__main__":
    run_sandbox(MOD1)

