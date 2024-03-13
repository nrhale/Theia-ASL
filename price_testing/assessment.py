# This file will have a camera open, take in a single frame after 5 seconds, and see if it is the right symbol
import random
import time
import cv2
from price_testing.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math

from price_testing.save_load2 import*
from price_testing.sign_info import*
from price_testing.common import*

TIMER_TIME = 5

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
            try:
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
            except:
                print("get back in range")

        else:
            try:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize
                #print("yo")
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


# Choosing a random symbol from sign list
def choose_symbol(sym_list):
    chosen_sym = random.choice(sym_list)
    sym_list.remove(chosen_sym) #should probably be done after
    return chosen_sym

def smart_choose(sym_list):
    chosen_sym = sym_list[0]
    sym_list.remove(chosen_sym) #should probably be done after
    return chosen_sym

# returns the associated sign predicted from an image
def get_prediction(sign_list, image, classifier):
    if image is None:
        #raise TypeError("Last image had no hand")
        print("Last image had no hand")
        return None
    prediction, index = classifier.getPrediction(image)
    sign_seen = sign_list[index]
    return sign_seen

# Returns the final image of 5s period. Adds overlay so the output can be used in prediction
def assess_sign(model_name):
    cap = cv2.VideoCapture(0)

    detector = HandDetector(maxHands=1)  # may change later
    classifier = Classifier(f"{model_name}/keras_model.h5", f"{model_name}/labels.txt")
    imgSize = 300

    current_img = capture_video(cap, detector, imgSize, classifier)

    start_time = time.time()
    end_time = time.time()
    elapsed_time = end_time - start_time

    while elapsed_time < TIMER_TIME:
        end_time = time.time()
        elapsed_time = end_time - start_time
        # update video
        current_img = capture_video(cap, detector, imgSize, classifier)
    return current_img

# Main assessment loop. Pass in a module and it will ask you each sign you have learned
def full_process(module):

    remaining_list = module.sign_name_list.copy()
    model_name = module.model
    #sign_name_list = module.sign_name_list
    sign_name_list = create_si_name_list(SI_LIST, module.module_name)
    score = 0
    while len(remaining_list) > 0:
        classifier = Classifier(f"{model_name}/keras_model.h5", f"{model_name}/labels.txt")
        chosen_sign = choose_symbol(remaining_list) # also removes from remaining list, but should probably decouple this
        print(f"Please Sign {chosen_sign}")
        user_img = assess_sign(model_name)
        prediction = get_prediction(sign_name_list, user_img, classifier)
        score = compare_signs(chosen_sign, prediction, score, module.sign_list) # returns new score (incremented by 1 if correct)
        input("Press enter to continue (in react this will be waiting for 'next' button to be pressed)")
        #print(f"Prediction is {prediction}")
    print(f"Score: {score}/{len(module.sign_name_list)}")
    update_high_score(score, module)

def smart_assessment(module):

    remaining_list = order_sign_by_accuracy(module)
    model_name = module.model
    #sign_name_list = module.sign_name_list
    sign_name_list = create_si_name_list(SI_LIST, module.module_name)
    score = 0
    while len(remaining_list) > 0:
        classifier = Classifier(f"{model_name}/keras_model.h5", f"{model_name}/labels.txt")
        chosen_sign = smart_choose(remaining_list) # also removes from remaining list, but should probably decouple this
        print(f"Please Sign {chosen_sign}")
        user_img = assess_sign(model_name)
        prediction = get_prediction(sign_name_list, user_img, classifier)
        score = compare_signs(chosen_sign, prediction, score, module.sign_list) # returns new score (incremented by 1 if correct)
        input("Press enter to continue (in react this will be waiting for 'next' button to be pressed)")
        #print(f"Prediction is {prediction}")
    print(f"Score: {score}/{len(module.sign_name_list)}")

    update_high_score2(score, module)

def rounds_assessment(module):
    wrong_list = [] # used for storing signs the user got wrong
    remaining_list = module.sign_name_list.copy()
    model_name = module.model
    #sign_name_list = module.sign_name_list
    sign_name_list = create_si_name_list(SI_LIST, module.module_name)
    score = 0
    while len(remaining_list) > 0:
        classifier = Classifier(f"{model_name}/keras_model.h5", f"{model_name}/labels.txt")
        chosen_sign = choose_symbol(remaining_list) # also removes from remaining list, but should probably decouple this
        print(f"Please Sign {chosen_sign}")
        user_img = assess_sign(model_name)
        prediction = get_prediction(sign_name_list, user_img, classifier)
        score_before = score
        score = compare_signs(chosen_sign, prediction, score, module.sign_list) # returns new score (incremented by 1 if correct)
        if score == score_before:
            wrong_list.append(chosen_sign)
        input("Press enter to continue (in react this will be waiting for 'next' button to be pressed)")
        #print(f"Prediction is {prediction}")
    print(f"Score: {score}/{len(module.sign_name_list)}")
    update_high_score3(score, module)
    print("REDEMPTION ROUND")
    while len(wrong_list) > 0:
        classifier = Classifier(f"{model_name}/keras_model.h5", f"{model_name}/labels.txt")
        chosen_sign = choose_symbol(wrong_list) # also removes from remaining list, but should probably decouple this
        print(f"Please Sign {chosen_sign}")
        user_img = assess_sign(model_name)
        prediction = get_prediction(sign_name_list, user_img, classifier)
        score_before = score
        score = compare_signs(chosen_sign, prediction, score, module.sign_list) # returns new score (incremented by 1 if correct)
        if score == score_before:
            wrong_list.append(chosen_sign)
        input("Press enter to continue (in react this will be waiting for 'next' button to be pressed)")
        #print(f"Prediction is {prediction}")

def survival_assessment(module):
    lives_left = LIVES
    score = 0
    ##print(f"Lives: {lives_left}")
    while lives_left > 0:
        print(f"Lives: {lives_left}")
        remaining_list = module.sign_name_list.copy()
        model_name = module.model
        #sign_name_list = module.sign_name_list
        sign_name_list = create_si_name_list(SI_LIST, module.module_name)
        while len(remaining_list) > 0:
            classifier = Classifier(f"{model_name}/keras_model.h5", f"{model_name}/labels.txt")
            chosen_sign = choose_symbol(remaining_list) # also removes from remaining list, but should probably decouple this
            print(f"Please Sign {chosen_sign}")
            user_img = assess_sign(model_name)
            prediction = get_prediction(sign_name_list, user_img, classifier)
            score_before = score
            score = compare_signs(chosen_sign, prediction, score,
                                  module.sign_list)  # returns new score (incremented by 1 if correct)
            if score == score_before:
                print("Life Lost!")
                lives_left -= 1
                if lives_left <= 0:
                    break
            input("Press enter to continue (in react this will be waiting for 'next' button to be pressed)")
            #print(f"Prediction is {prediction}")
    print(f"Score: {score}/{len(module.sign_name_list)}")
    update_high_score4(score, module)
def order_sign_by_accuracy(module):
    acc_ordered_list = []
    sign_ordered_list = []
    for sign in module.sign_list:
        if sign.assessed_count == 0:
            acc_ordered_list.insert(0, 0)
            sign_ordered_list.insert(0, sign.sign_name)
        elif len(acc_ordered_list) == 0:
            acc = sign.correct_count / sign.assessed_count
            sign_ordered_list.append(sign.sign_name)
            acc_ordered_list.append(acc)
        else:
            acc = sign.correct_count/sign.assessed_count
            for i in range(0, len(acc_ordered_list)):
                if acc <= acc_ordered_list[i]:
                    acc_ordered_list.insert(i, acc)
                    sign_ordered_list.insert(i, sign.sign_name)
                    break
    return sign_ordered_list



# Used specifically for learning process
def learn_sign(module, chosen_sign):
    score = 0
    model_name = module.model
    sign_name_list = create_si_name_list(SI_LIST, module.module_name) # this may have to be used as the sign list in full_process as well
    classifier = Classifier(f"{model_name}/keras_model.h5", f"{model_name}/labels.txt")
    print(f"Please Sign {chosen_sign}")
    user_img = assess_sign(model_name)
    prediction = get_prediction(sign_name_list, user_img, classifier)
    score = compare_signs_learn(chosen_sign, prediction, score)  # returns new score (incremented by 1 if correct)
    if score == 1:
        add_new_sign(module, chosen_sign)




def compare_signs(system_sign, user_sign, score, sign_list):
    if (system_sign == user_sign):
        print("Correct!")
        update_sign_data(system_sign, True, sign_list)
        score += 1
        # also remove from list or add to a new list for end-of-session testing of missed signs
    elif (user_sign == None):
        print("Sorry! No hand was detected in the frame.")
    else:
        update_sign_data(system_sign, False, sign_list)
        print(f"Sorry! It looks like the sign you made was {user_sign}.")
    return score

#similar function but used in learning process (ignores update)
def compare_signs_learn(system_sign, user_sign, score):
    if (system_sign == user_sign):
        print("Correct!")
        score += 1
        # also remove from list or add to a new list for end-of-session testing of missed signs
    elif (user_sign == None):
        print("Sorry! No hand was detected in the frame.")
    else:
        print(f"Sorry! It looks like the sign you made was {user_sign}.")
    return score



# Update sign user data
def update_sign_data(sign_name, is_correct, sign_list):

    # First get the sign object based on sign name
    sign = find_sign(sign_name, sign_list)

    # Update sign information
    sign.assessed_count += 1
    if (is_correct == True):
        sign.correct_count += 1

#combine all this into one function later. Just wanted to try quickly
def update_high_score(score, module):
    if(score > module.high_score):
        print("new high score!")
        module.high_score = score

def update_high_score2(score, module):
    if(score > module.high_score2):
        print("new high score!")
        module.high_score2 = score

def update_high_score3(score, module):
    if(score > module.high_score3):
        print("new high score!")
        module.high_score3 = score

def update_high_score4(score, module):
    if(score > module.high_score4):
        print("new high score!")
        module.high_score4 = score


# Find a sign object in a list of Sign objects when given its name
def find_sign(sign_wanted, sign_list):
    for s in sign_list:
        if s.sign_name == sign_wanted:
            return s
    raise ValueError("There is no sign with this name within the sign list")


# Used when a sign is learned to add it to the user's know signs
def add_new_sign(module, chosen_sign):
    for s in module.sign_name_list:
        if s == chosen_sign:
            return
    new_sign = Sign(chosen_sign, 0, 0, module.module_name)
    module.sign_list.append(new_sign) # adding sign to sign list
    module.sign_name_list.append(new_sign.sign_name) # adding sign name to sign name list








if __name__ == "__main__":
    print("hi")
    """
    #assess_sign("A")
    #sign_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "O", "P", "Q", "R", "S"]

    s1 = Sign("A", 10, 9, "alphabet1")
    s2 = Sign("B", 5, 4, "alphabet1")
    s3 = Sign("C", 10, 4, "alphabet1")

    s4 = Sign("D", 2, 1, "alphabet2")
    s5 = Sign("E", 3, 2, "alphabet2")
    s6 = Sign("F", 5, 4, "alphabet2")

    s_list1 = [s1]
    s_list2 = [s4, s5, s6]

    mod_list = []
    mod1 = Module("alphabet1", "model3", s_list1, 0)
    mod2 = Module("alphabet2", "model3", s_list2, 2)
    mod_list.append(mod1)
    mod_list.append(mod2)

    sign_list = ["A", "B", "C"]
    """
    loaded_modules = load_module_objects("oddy_data")
    username = "price"
    #loaded_module_list, loaded_sign_list = load_user_data(f"{username}.json")

    #full_process(loaded_modules[0])
    survival_assessment(loaded_modules[0])
    save_module_data(loaded_modules, "oddy_data")
    print("hi")






