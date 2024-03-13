# app.py
from flask import Flask, render_template, request, jsonify
from price_testing.common import*
from price_testing.assessment import*


app = Flask(__name__)

# Your existing function (full_process) goes here
def full_process2(module):

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
        print("Press enter to continue (in react this will be waiting for 'next' button to be pressed)")
        #print(f"Prediction is {prediction}")
    print(f"Score: {score}/{len(module.sign_name_list)}")
    update_high_score(score, module)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_full_process', methods=['POST'])
def run_full_process():
    full_process2(MOD1)
    result = "Example Result"
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)

