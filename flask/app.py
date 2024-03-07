from flask import Flask, render_template, request
import json
from static.data.modules import get_modules
from static.data.assessments import get_assessments

username = None


app = Flask(__name__)


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/home", methods=["POST"])
def home():
    global username
    username = request.form["username"]
    return render_template("home.html", username=username)


@app.route("/statistics")
def statistics():
    # TODO: Do not hardcode the path
    with open("../price_testing/mp_data.json") as f:
        statistics = json.load(f)
    return render_template("statistics.html", username=username, statistics=statistics)


@app.route("/modules")
def modules():
    modules = get_modules()
    assessments = get_assessments()
    return render_template("modules.html", modules=modules, assessments=assessments)


@app.route("/learn/<module>/<sign>")
def learn(module, sign):
    return render_template("learn.html", module=module, sign=sign)


@app.route("/assessment/<module>/<assessmentType>")
def assessment(module, assessmentType):
    return render_template(
        "assessment.html", module=module, assessmentType=assessmentType
    )


@app.route("/sandbox/<module>")
def sandbox(module):
    return render_template("sandbox.html", module=module)


if __name__ == "__main__":
    app.run(debug=True)
