from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def signin():
    return "<h1>Sign In</h1>"

if __name__ == '__main__':
    app.run(debug=True)
