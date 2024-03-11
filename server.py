from flask import Flask
from flask import request
from flask import render_template
import json
app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    #load a current view of the data
    f = open("data/life_expectancy.json", "r")
    data = json.load(f)
    f.close()
    years=sorted(list(data["Canada"].keys()))

    p_years = []
    for year in years:
        p_years.append(int(year)-1960)

    Can_line_endpoints = []
    Us_line_endpoints = []
    Mex_line_endpoints = []
    for country in data:
        for i in range(len(data[country])-1): # make it easy to dynamically generate a line graph
            start_x = years[i] #generate endpoints for each line segment
            stop_x = years[i+1]
            if country == "Canada":
                Can_line_endpoints.append([data[country][start_x],data[country][stop_x]])
            elif country == "United States":
                Us_line_endpoints.append([data[country][start_x],data[country][stop_x]])
            else:
                Mex_line_endpoints.append([data[country][start_x],data[country][stop_x]])

    print(Can_line_endpoints, Us_line_endpoints, Mex_line_endpoints)
    #render the template with the apporpriate data
    return render_template('index.html', p_years = p_years, data = data, years=years, Can_line_endpoints = Can_line_endpoints, Us_line_endpoints = Us_line_endpoints, Mex_line_endpoints = Mex_line_endpoints)


@app.route('/year')
def all_scores():
    #load a current view of the data
    f = open("data/life_expectancy.json", "r")
    data = json.load(f)
    f.close()

    #check to see if year is in the query string portion of the URL
    requested_year = request.args.get('year')
    if requested_year == None:
        requested_year = "2020" #just in case

    #Filter and reformat data for ease of access in the template
    countries = list(data.keys())
    requested_data = {}
    for country in countries:
        requested_data[country] = data[country][requested_year]
    all_years = sorted(list(data[countries[0]].keys()))

    return render_template('all_scores.html', year=requested_year, all_years=all_years, data=requested_data)
app.run(debug=True)
