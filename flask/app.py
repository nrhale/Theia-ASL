from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/statistics")
def statistics():
    return render_template("statistics.html")


@app.route("/modules")
def modules():
    return render_template("modules.html")


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
