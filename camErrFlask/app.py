from flask import Flask, render_template, Response
import cv2
from price_testing.assessment import *

app = Flask(__name__)
#camera = cv2.VideoCapture(0)

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    return Response(generate_frames(cap, detector), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)