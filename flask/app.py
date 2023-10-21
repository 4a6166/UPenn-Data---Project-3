from flask import Flask, render_template, jsonify, url_for  # Lesson 10-3
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.sql import func
import json

# connect to DB
engine = create_engine("sqlite:///pa_school_district.db")
Base = automap_base()
Base.prepare(autoload_with=engine)
print(Base.classes.keys())

session = Session(engine)


######################################################################
# FLASK
######################################################################
# initiate flask app
app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')


# set up primary/only route
@app.route("/")
def home():
    # log to console that route connected
    print("App running")

    results = []
    table = session.query(Base.classes.pa_schools.County,
                          Base.classes.pa_schools.AUN,
                          func.sum(Base.classes.keystone_biology.Advanced + Base.classes.keystone_biology.Proficient)
                          ).group_by(Base.classes.pa_schools.County)

    for row in table:
        r = []
        for cell in row:
            r.append(cell)
        results.append(r)
        # results.append({"County": row[0], "AUN": row[1]})

    # render the dashboard template
    return render_template("home.html", query_results=results)


# Run a query from a POST
@app.route("/post/<post_id>")
def get_post(post_id):

    def parse_post(post_id):
        # do something to get query out of post
        return post_id

    query = parse_post(post_id)

    def run_query(query):
        # run a query
        return query

    return render_template("home.html", query_result=run_query(query))


# Provide an API
@app.route("/api/test")
def api_test():

    results = ['Populate this with new dics for all the data needed to pass',
               ['nested', 'lists', 'work'],
               {'1. dictionaries': 'Work here too!',
                '2. as do': {'nested': 'dicts'}
                },
               'So, tell me what data you need and I\'ll serve it through a variable',
               'specifically "query_results',
               'and it will pull in for each page'
               ]

    return jsonify(results)


# calls the geojson file and passes it to a js var
@app.route("/map")
def get_map():
    results = 'RESULTS'
    boundaries = ''

    with open('static/Pennsylvania School Districts Boundaries.geojson') as file:
        boundaries = json.load(file)

    return render_template("map.html", query_results=results, boundaries=boundaries)


@app.route("/scatter")
def get_scatter():
    return render_template("scatter.html")


@app.route("/slope")
def get_slope():
    return render_template("slope.html")


@app.route("/radar")
def get_radar():
    return render_template("radar.html")


# set debugger
if __name__ == "main":
    app.run(debug=True)

