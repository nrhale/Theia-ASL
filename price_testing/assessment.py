#This file will have a video playing, take in a single frame after 5 seconds, and see if it is the right symbol
import random
import time
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math

#choose a symbol and remove it from the list, return

def capture_video(cap, detector, imgSize, classifier):
    offset = 20
    success, img = cap.read()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]  # because we just have the one hand
        x, y, w, h = hand['bbox']  # gets us all the values

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255  # imgSize x imgSize square
        # np.uint8 restricts it to 8 bits (0 to 255)
        imgCrop = img[y - offset:y + h + offset,
                  x - offset:x + w + offset]  # starting height, ending height, starting width, ending width

        imgCropShape = imgCrop.shape
        # imgWhite[0:imgCropShape[0], 0:imgCropShape[1]] = imgCrop

        aspectRatio = h / w

        if aspectRatio > 1:
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
            prediction, index = classifier.getPrediction(imgWhite)
            #letter_seen = labels[index]
            #print(f"Detected letter: {letter_seen}")
            #print(prediction, index)
        # print(index)

        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize - hCal) / 2)
            try:
                imgWhite[hGap:hCal + hGap, :] = imgResize
                print("yo")
                prediction, index = classifier.getPrediction(imgWhite)
                #letter_seen = labels[index]
                #print(f"Detected letter: {letter_seen}")
                #print(prediction, index)
            except:
                print("get back in range")

        #cv2.imshow("ImageCrop", imgCrop)
        #cv2.imshow("ImageWhite", imgWhite)
    else:
        imgWhite = None
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    return imgWhite


def choose_symbol(sym_list):
    chosen_sym = random.choice(sym_list)
    sym_list.remove(chosen_sym)
    return chosen_sym

#retruns the associated sign predicted from an image
def get_prediction(sign_list, image, classifier):
    if image is None:
        raise TypeError("Last image had no hand")
    prediction, index = classifier.getPrediction(image)
    sign_seen = sign_list[index]
    return sign_seen

# chooses a sign and
def assess_sign(sign, model_name):
    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=1)  # may change later
    classifier = Classifier(f"{model_name}/keras_model.h5", f"{model_name}/labels.txt")
    imgSize = 300

    current_img = capture_video(cap, detector, imgSize, classifier)

    start_time = time.time()
    end_time = time.time()
    elapsed_time = end_time - start_time

    while elapsed_time < 5:
        end_time = time.time()
        elapsed_time = end_time - start_time
        #update video
        current_img = capture_video(cap, detector, imgSize, classifier)
        #print e
        pass
    return current_img

def full_process(sign_list, model_name):

    remaining_list = sign_list.copy()
    classifier = Classifier(f"{model_name}/keras_model.h5", f"{model_name}/labels.txt")
    chosen_sign = choose_symbol(remaining_list) #also removes from remaining list, but should probably decouple this
    user_img = assess_sign(chosen_sign, model_name)
    prediction = get_prediction(sign_list, user_img, classifier)
    print(f"Prediction is {prediction}")




if __name__ == "__main__":
    print("hi")
    #assess_sign("A")
    sign_list = ["A", "B", "C"]
    full_process(sign_list, "model3")






