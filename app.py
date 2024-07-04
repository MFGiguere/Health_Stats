"""
source venv/Scripts/activate
export FLASK_DEBUG=1
flask run
"""

from flask import Flask, render_template, make_response
import csv, re

"Create some categories and basic work"
category = ["Health", "Sports", "Socio-demographic", "Nutrition", "Social habits"]

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('base.html', category=category)

@app.route('/admin')
def admin():
    data = "import something from csv"
    return render_template(f'admin.html', category=category)

@app.route('/<cat>')
def display(cat):
    data = "import something from csv"
    return make_response(render_template(f'category.html', cat=cat, category=category))

if __name__ == '__main__':
   app.run(debug=True)   