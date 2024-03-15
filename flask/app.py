# Built-in packages
import json
import sys
import os

# pip packages
from flask import Flask, redirect, render_template, request, url_for, Response
import cv2

# Add the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Our packages
from price_testing.sandbox import run_sandbox
from price_testing.assessment import *
from static.data.modules import get_modules
from static.data.assessments import get_assessments
from price_testing.common import *

# Use these as global variables. There may be more
username = None
statistics = None
mod_list = None
user_mod_data = []
si = None
chosen_mod = None
chosen_sign = None

app = Flask(__name__)
# camera = cv2.VideoCapture(0)


# cap = cv2.VideoCapture(0)
# detector = HandDetector(maxHands=1)
print("SANDBOX FLASK")


def generate_output(module):
    # Your while loop logic here
    remaining_list = module.sign_name_list.copy()
    model_name = module.model
    sign_name_list = create_si_name_list(SI_LIST, module.module_name)
    score = 0

    while len(remaining_list) > 0:
        classifier = Classifier(
            f"{model_name}/keras_model.h5", f"{model_name}/labels.txt"
        )
        chosen_sign = choose_symbol(remaining_list)

        # Yield the "Please sign {chosen_sign}" message for SSE
        yield f"data: Please sign {chosen_sign}\n\n"

        # Now assess the sign
        user_img = assess_sign(model_name)
        # cv2.destroyAllWindows()
        prediction = get_prediction(sign_name_list, user_img, classifier)
        old_score = score
        score = compare_signs(chosen_sign, prediction, score, module.sign_list)
        if old_score == score:
            yield f"data: Sorry! It looks like the sign you made was {prediction}.\n\n"
        else:
            yield f"data: Correct!\n\n"

        # If desired, you can add a delay here before the next iteration
        # (e.g., time.sleep(1) for a 1-second delay)

    # Yield the final score
    yield f"data: Score: {score}/{len(module.sign_name_list)}\n\n"


@app.route("/a_test")
def a_test():
    return render_template("sse_output.html")


@app.route("/sse_output")
def sse_output():
    return Response(generate_output(MOD1), content_type="text/event-stream")


def generate_frames():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=1)
    while True:
        # success, frame = camera.read()
        success, img = cap.read()
        if not success:
            break

        offset = 20
        hands, img = detector.findHands(img)

        # Encode frame to JPEG
        ret, jpeg = cv2.imencode(".jpg", img)
        if not ret:
            break

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
        )


def live_sandbox(module):
    labels = create_si_name_list(SI_LIST, module.module_name)

    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=1)  # may change later

    classifier = Classifier(
        f"{module.model}/keras_model.h5", f"{module.model}/labels.txt"
    )

    imgSize = 300
    # create offset for crop size
    offset = 20
    lol = True
    while lol == True:
        # success, frame = camera.read()
        success, img = cap.read()
        if not success:
            break

        offset = 20
        hands, img = detector.findHands_sandbox(img)

        # sandbox stuff
        if hands:
            hand = hands[0]  # because we just have the one hand
            x, y, w, h = hand["bbox"]  # gets us all the values

            # making all images the same size

            imgWhite = (
                np.ones((imgSize, imgSize, 3), np.uint8) * 255
            )  # imgSize x imgSize square
            imgCrop = img[
                y - offset : y + h + offset, x - offset : x + w + offset
            ]  # starting height, ending height, starting width, ending width

            imgCropShape = imgCrop.shape
            aspectRatio = h / w

            if aspectRatio > 1:
                try:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                    imgResizeShape = imgResize.shape
                    wGap = math.ceil((imgSize - wCal) / 2)
                    imgWhite[:, wGap : wCal + wGap] = imgResize
                    prediction, index = classifier.getPrediction(imgWhite)
                    letter_seen = labels[index]
                    print(f"Detected letter: {letter_seen}")
                    cv2.putText(
                        img,
                        labels[index],
                        (x - 30, y - 30),
                        cv2.FONT_HERSHEY_PLAIN,
                        6,
                        (0, 0, 0),
                        2,
                    )
                except:
                    print("get back in range")
            else:
                try:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    imgResizeShape = imgResize.shape
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap : hCal + hGap, :] = imgResize
                    prediction, index = classifier.getPrediction(imgWhite)
                    letter_seen = labels[index]
                    print(f"Detected letter: {letter_seen}")
                    cv2.putText(
                        img,
                        labels[index],
                        (x - 30, y - 30),
                        cv2.FONT_HERSHEY_PLAIN,
                        6,
                        (0, 0, 0),
                        2,
                    )
                except:
                    print("get back in range")

        # Encode frame to JPEG
        ret, jpeg = cv2.imencode(".jpg", img)
        if not ret:
            break

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
        )


@app.route("/video")
def vids():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/<module>/video")
def video(module):
    chosen_mod = search_mod_for_name(module, user_mod_data)
    return Response(
        live_sandbox(chosen_mod), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# global username
# user_id = None


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/sandbox/<module>")
def index(module):
    return render_template("sandboxv2.html", module=module)


@app.route("/register", methods=["POST"])
def register():
    global username
    global user_mod_data
    username = request.form["username"]
    if os.path.isfile(f"../user_files/{username}_data.json") == False:
        print("new user!")
        mod_list = [
            MOD1,
            MOD2,
            MOD3,
            MOD4,
            MOD5,
            MOD6,
        ]  # from common. Load new user with starter modules
        save_module_data(mod_list, f"{username}_data")
    user_mod_data = load_module_objects(f"{username}_data")
    return redirect(url_for("home"))


@app.route("/home")
def home():
    global username
    return render_template("home.html", username=username)


@app.route("/statistics")
def statistics():
    with open(f"../user_files/{username}_data.json") as f:
        statistics = json.load(f)
    return render_template("statistics.html", username=username, statistics=statistics)


@app.route("/modules")
def modules():
    modules = get_modules()
    assessments = get_assessments()
    return render_template("modules.html", modules=modules, assessments=assessments)


@app.route("/learn/<module>/<sign>")
def learn(
    module,
    sign,
    result="Press 'Try Sign' and then hold up the sign. The capturing Process may taking a few seconds.",
):
    global chosen_mod
    chosen_mod = search_mod_for_name(module, user_mod_data)
    global chosen_sign
    chosen_sign = sign
    return render_template("learn.html", module=module, sign=sign, result=result)


@app.route("/assessment/<module>/<assessmentType>")
def assessment(module, assessmentType):
    return render_template(
        "assessment.html", module=module, assessmentType=assessmentType
    )


@app.route("/run_sandbox_f", methods=["POST"])
def run_sandbox_f():
    # Call your run_sandbox(chosen_mod) function here
    # Replace the following line with your actual logic
    result = run_sandbox(chosen_mod)  # Replace with your function call
    return f"Sandbox executed with result: {result}"


@app.route("/<module>/<sign>/run_learn_sign_f", methods=["POST"])
def run_learn_sign_f(module, sign):
    # Call your run_sandbox(chosen_mod) function here
    # Replace the following line with your actual logic
    res = learn_sign(chosen_mod, chosen_sign)  # Replace with your function call
    save_module_data(user_mod_data, f"{username}_data")
    return render_template("learn.html", module=module, sign=sign, result=res)


@app.route("/looper")
def looper():
    return render_template("loop.html")


@app.route("/run_while_loop", methods=["POST"])
def run_while_loop():
    # Get the current iteration count from the request
    count = int(request.form.get("count", 0))

    # Your while loop logic here
    if count < 10:
        count += 1
        return str(count)  # Return the updated iteration count
    else:
        return "Loop completed"


if __name__ == "__main__":
    app.run(debug=True)
