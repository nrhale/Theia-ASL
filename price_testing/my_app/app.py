# app.py

from flask import Flask, render_template

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Module list page
@app.route('/modules')
def modules():
    return render_template('modules.html')

# Module details page
@app.route('/module/<int:module_id>')
def module_details(module_id):
    # Retrieve module details based on module_id
    # You can use a database or any other data source
    # For now, let's assume you have a dictionary of modules
    modules = {
        1: {'name': 'Module 1', 'description': 'Learn something'},
        2: {'name': 'Module 2', 'description': 'Explore more'},
        # Add more modules here
    }
    module = modules.get(module_id)
    return render_template('module_details.html', module=module)

if __name__ == '__main__':
    app.run(debug=True)