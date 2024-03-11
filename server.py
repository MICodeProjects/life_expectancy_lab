# flask --app data_server run
from flask import Flask
from flask import render_template
import json


app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    #load a current view of the data
    f = open("data/life_expectancy.json", "f")
    data = json.load(f)
    f.close()

    #render the template with the apporpriate data
    return render_template('index.html')

@app.route('/year')
def year():
    return render_template('year.html')

app.run(debug=True)