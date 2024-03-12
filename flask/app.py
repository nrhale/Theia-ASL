from flask import Flask, render_template, request
import json

from price_testing.sandbox import run_sandbox
from static.data.modules import get_modules
from static.data.assessments import get_assessments
from price_testing.common import*

#Use these as global variables. There may be more
username = None
mod_list = None
user_mod_data = []
si = None

#global username
#user_id = None


app = Flask(__name__)


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
def learn(module, sign):
    return render_template("learn.html", module=module, sign=sign)


@app.route("/assessment/<module>/<assessmentType>")
def assessment(module, assessmentType):
    return render_template(
        "assessment.html", module=module, assessmentType=assessmentType
    )


@app.route("/sandbox/<module>")
def sandbox(module):
    print(module)
    #mod_index = list_modules(user_mod_data)
    #chosen_mod = user_mod_data[mod_index]
    print("SANDBOX")
    #run_sandbox(chosen_mod)
    return render_template("sandbox.html", module=module)


if __name__ == "__main__":
    app.run(debug=True)
