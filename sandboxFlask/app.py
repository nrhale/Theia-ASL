from flask import Flask, render_template, Response, request
import cv2
from price_testing.assessment import *
from price_testing.sandbox import run_sandbox
from price_testing.common import*
from price_testing.assessment import*
from static.data.modules import get_modules
from static.data.assessments import get_assessments
username = None
mod_list = None
user_mod_data = []
si = None
chosen_mod = None
chosen_sign = None

app = Flask(__name__)
#camera = cv2.VideoCapture(0)



#cap = cv2.VideoCapture(0)
#detector = HandDetector(maxHands=1)
print("SANDBOX FLASK")

"""
def generate_frames(cap, detector):
    while True:
        #success, frame = camera.read()
        success, img = cap.read()
        if not success:
            break

        offset = 20
        hands, img = detector.findHands(img)

        # Encode frame to JPEG
        ret, jpeg = cv2.imencode('.jpg', img)
        if not ret:
            break

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
"""

def live_sandbox(module):
    labels = create_si_name_list(SI_LIST, module.module_name)

    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=1)  # may change later

    classifier = Classifier(f"{module.model}/keras_model.h5", f"{module.model}/labels.txt")

    imgSize = 300
    # create offset for crop size
    offset = 20
    lol = True
    while lol == True:
        #success, frame = camera.read()
        success, img = cap.read()
        if not success:
            break

        offset = 20
        hands, img = detector.findHands_sandbox(img)

        #sandbox stuff
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


        # Encode frame to JPEG
        ret, jpeg = cv2.imencode('.jpg', img)
        if not ret:
            break


        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

"""

@app.route('/video')
def video():
    return Response(generate_frames(cap, detector), mimetype='multipart/x-mixed-replace; boundary=frame')
"""
@app.route('/video')
def video():
    chosen_mod = search_mod_for_name("The Alphabet I", user_mod_data)
    return Response(live_sandbox(chosen_mod), mimetype='multipart/x-mixed-replace; boundary=frame')




#global username
#user_id = None



@app.route("/")
def login():
    return render_template("login.html")

"""
@app.route("/home", methods=["POST"])
def home():
    global username
    username = request.form["username"]
    return render_template("home.html", username=username)
"""

@app.route('/ha')
def index():
    return render_template('index.html')


@app.route("/home", methods=["POST"])
def home():
    global username
    global user_mod_data
    username = request.form["username"]
    if os.path.isfile(f"../user_files/{username}_data.json") == False:
        print("new user!")
        mod_list = [MOD1, MOD2, MOD3, MOD4, MOD5, MOD6]  # from common. Load new user with starter modules
        save_module_data(mod_list, f"{username}_data")
    user_mod_data = load_module_objects(f"{username}_data")
    return render_template("home.html", username=username)


@app.route("/statistics")
def statistics():
    # TODO: Do not hardcode the path
    with open(f"../user_files/{username}_data.json") as f:
        statistics = json.load(f)
    return render_template("statistics.html", username=username, statistics=statistics)


@app.route("/modules")
def modules():
    modules = get_modules()
    assessments = get_assessments()
    return render_template("modules.html", modules=modules, assessments=assessments)


@app.route("/learn/<module>/<sign>")
def learn(module, sign, result="No Result Yet"):
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


@app.route("/sandbox/<module>")
def sandbox(module):
    print(module)
    global chosen_mod
    #mod_index = list_modules(user_mod_data)
    #chosen_mod = user_mod_data[mod_index]
    chosen_mod = search_mod_for_name(module, user_mod_data)
    print("SANDBOX")
    #run_sandbox(chosen_mod)
    return render_template("sandbox.html", module=module)

@app.route('/run_sandbox_f', methods=['POST'])
def run_sandbox_f():
    # Call your run_sandbox(chosen_mod) function here
    # Replace the following line with your actual logic
    result = run_sandbox(chosen_mod)  # Replace with your function call
    return f"Sandbox executed with result: {result}"

@app.route('/<module>/<sign>/run_learn_sign_f', methods=['POST'])
def run_learn_sign_f(module, sign):
    # Call your run_sandbox(chosen_mod) function here
    # Replace the following line with your actual logic
    res = learn_sign(chosen_mod, chosen_sign)  # Replace with your function call
    save_module_data(user_mod_data, f"{username}_data")
    return render_template("learn.html", module=module, sign=sign, result=res)


if __name__ == "__main__":
    app.run(debug=True)
