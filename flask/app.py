# built-in packages
import json
import sys
import os

# pip packages
from flask import Flask, redirect, render_template, request, url_for

# Add the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Our packages
from price_testing.sandbox import run_sandbox
from static.data.modules import get_modules
from static.data.assessments import get_assessments

from price_testing.common import*
from price_testing.assessment import*

# Use these as global variables. There may be more
username = None
statistics = None

mod_list = None
user_mod_data = []
si = None
chosen_mod = None
chosen_sign = None

# global username
# user_id = None


app = Flask(__name__)


@app.route("/")
def login():
    return render_template("login.html")


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
    chosen_mod = search_mod_for_name(module, user_mod_data)
    print("SANDBOX")
    # run_sandbox(chosen_mod)
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
