from flask import Flask, request, render_template, jsonify, url_for  # Lesson 10-3
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.sql import func
import json

# imports for scatter
import pandas as pd
import plotly.express as px

# connect to DB
engine = create_engine("sqlite:///pa_school_district.db")
Base = automap_base()
Base.prepare(autoload_with=engine)

# TODO: should this be moved to open and close at each route?
session = Session(engine)


######################################################################
# FLASK
######################################################################
# initiate flask app
app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')


######################################################################
# Serves the API
######################################################################
# API for map views
@app.route("/api/map", methods=['GET'])
def get_map_api():
    view = request.args.get('view', None)

    # return list of dicst with AUN, District, Advanced, Proficient, NumeberScored, and Total (Advanced + Proficient)
    def query_scores(s):
        result = []

        query = session.query(
                           Base.classes[s].AUN,
                           func.avg(Base.classes[s].Advanced),
                           func.avg(Base.classes[s].Proficient),
                           func.sum(Base.classes[s].NumberScored),
                           func.avg(
                               (Base.classes[s].Advanced) + 
                               (Base.classes[s].Proficient)
                               ),
                           Base.classes.pa_schools.District
                           ).join(Base.classes.pa_schools,
                                  Base.classes[s].AUN == Base.classes.pa_schools.AUN
                           ).group_by(Base.classes[s].AUN)

        for row in query:
            r = {
                    'AUN': row[0],
                    'District': row[5],
                    'Advanced': row[1],
                    'Proficient': row[2],
                    'NumberScored': row[3],
                    'Total': row[4]
                }
            result.append(r)

        return result

    results = []

    if view == "pupil":
        query = session.query(Base.classes.person_spend.AUN,
                              Base.classes.person_spend.LocalPupil,
                              Base.classes.person_spend.StatePupil,
                              Base.classes.person_spend.FedPupil
                              ).filter(Base.classes.person_spend.AUN != "103022253"
                              ).group_by(Base.classes.person_spend.AUN)

        for row in query:
            r = {
                'AUN': row[0],
                'LocalPupil': row[1],
                'StatePupil': row[2],
                'FedPupil': row[3],
                'Total': row[1]+row[2]+row[3]
            }
            results.append(r)
    elif view == "alg":
        results = query_scores("keystone_algebra")
    elif view == "bio":
        results = query_scores("keystone_biology")
    elif view == "lit":
        results = query_scores("keystone_literature")
    else:
        results = "Call pupil, alg, bio, or lit."

    return jsonify(results)


# API for scatter plots
@app.route("/api/scatter/pupil")
def get_scatter_pupil():
    results = []
    query = session.query(Base.classes.person_spend.AUN,
                          Base.classes.person_spend.LocalPupil,
                          Base.classes.person_spend.StatePupil,
                          Base.classes.person_spend.FedPupil
                          ).filter(Base.classes.person_spend.AUN != "103022253"
                                   ).group_by(Base.classes.person_spend.AUN).order_by(Base.classes.person_spend.AUN.desc())

    for row in query:
        results.append(row[1]+row[2]+row[3])

    return jsonify(results)


@app.route("/api/scatter", methods=['GET'])
def get_scatter_api():
    view = request.args.get('view', None)
    results = []

    query = session.query(
            func.avg(Base.classes[view].Proficient)
            ).join(Base.classes.person_spend,
                   Base.classes.person_spend.AUN == Base.classes[view].AUN
            ).group_by(Base.classes[view].AUN
            ).order_by(Base.classes.person_spend.AUN.desc())

    for row in query:
        results.append(row[0])

    return jsonify(results)


# API for slope
@app.route("/api/slope", methods=['GET'])
def get_slope_api():
    results = {}

    bio_prof = session.query(Base.classes.pa_schools.SchoolNumber,
                           Base.classes.pa_schools.AUN,
                           Base.classes.keystone_biology.Advanced,
                           Base.classes.keystone_biology.Proficient,
                           func.sum(Base.classes.keystone_biology.Advanced + Base.classes.keystone_biology.Proficient)
                           ).group_by(Base.classes.pa_schools.AUN)

    results["bio_prof"] = []
    for row in bio_prof:
        r = []
        for cell in row:
            r.append(cell)
        results["bio_prof"].append(r)

    alg_prof = session.query(Base.classes.pa_schools.SchoolNumber,
                           Base.classes.pa_schools.AUN,
                           func.sum(Base.classes.keystone_algebra.Advanced + Base.classes.keystone_algebra.Proficient)
                           ).group_by(Base.classes.pa_schools.AUN)

    results["alg_prof"] = []
    for row in alg_prof:
        r = []
        for cell in row:
            r.append(cell)
        results["alg_prof"].append(r)

    lit_prof = session.query(Base.classes.pa_schools.SchoolNumber,
                           Base.classes.pa_schools.AUN,
                           func.sum(Base.classes.keystone_literature.Advanced + Base.classes.keystone_literature.Proficient)
                           ).group_by(Base.classes.pa_schools.AUN)

    results["lit_prof"] = []
    for row in lit_prof:
        r = []
        for cell in row:
            r.append(cell)
        results["lit_prof"].append(r)

    return jsonify(results)


# API for radar
@app.route("/api/radar", methods=['GET'])
def get_radar_api():
    return "<p>Nothing here.<p>You feel a comfort in the quiet...<p>as if you never really wanted data for a radar chart at all."


# Basic SQL query example
@app.route("/api/example", methods=['GET'])
def example():
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

    return jsonify(results)


######################################################################
# Serves the webpages
######################################################################
@app.route("/")
def home():
    # render the dashboard template
    return render_template("home.html", data="")


# calls the geojson file and passes it to a js var
@app.route("/map")
def get_map():
    js_file = url_for('static', filename='map/app.js')
    # js_file = url_for('static', filename='map/andrew2.js')
    css_file = url_for('static', filename='map/andrew.css')
    data = ''
    with open('static/map/Pennsylvania_School_Districts_Boundaries.geojson') as file:
        data = json.load(file)

    note = '''
        <p class="mb-3">Use this map to explore how your school district compares to its neighboring districts and to the state overall.
        <p class="mb-3">Notice the clustering of Per Pupil Expenditure...
        <p class="mb-3">We see generally see the highest per pupil expenditures in Pittsburgh and its surrounding suburbs, in the Philadelphia suburbs but not the city itself, in Indiana and the surrounding districts, and in the fringes of the northeast. We generally see the lowest per pupil expenditures throughout south-central PA and the heart of the northeast.
        <p class="mb-3">However, we can see that academic Proficiency does not map directly onto these expenditure patterns by noticing how the geographical pattern of lowest per pupil expenditures \"disappears\" when viewing rates of Proficiency. One may expect that more money spent would result in better academic outcomes, but we are seeing that may not always be the case.
        <p>For that reason, we want to explore how related expenditure is to academic proficiency in Pennsylvania. Click onto the Scatter plot to explore this question.
           '''

    attribution = '''
        <p>This is 2018-2019 data from the
           <a class="underline"
              href="https://www.education.pa.gov/DataAndReporting/Pages/default.aspx"
               >
               Pennsylvania Department of Education
           </a>.
           The Proficiency data is from the Keystone Exams
           which replaced what many will know as the "PSSAs",
           and are administered to 11th graders
           (with some exceptions for those with special needs).
        '''

    controls = '''
        <!-- Code for tailwind radio buttons https://www.material-tailwind.com/docs/html/radio-button -->
        <div id="andrew" class="flex gap-10 radio-buttons-container">
          <div <h1>Select a Metric to View</h1></div>
          <div class="inline-flex items-center">
            <label
              class="relative flex cursor-pointer items-center rounded-full p-3 text-green-900 border-green-900"
              for="pupil"
              data-ripple-dark="true"
            >
              <input
                id="pupil"
                name="type"
                type="radio"
                class="before:content[''] peer relative h-5 w-5 cursor-pointer appearance-none rounded-full border border-blue-gray-200 text-green-900 transition-all before:absolute before:top-2/4 before:left-2/4 before:block before:h-12 before:w-12 before:-translate-y-2/4 before:-translate-x-2/4 before:rounded-full before:bg-blue-gray-500 before:opacity-0 before:transition-opacity checked:border-green-900 hover:before:bg-green-900 hover:before:opacity-10"
                checked
                />
              <div class="pointer-events-none absolute top-2/4 left-2/4 -translate-y-2/4 -translate-x-2/4 text-green-900 opacity-0 transition-opacity peer-checked:opacity-100">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-3.5 w-3.5"
                  viewBox="0 0 16 16"
                  fill="currentColor"
                >
                  <circle data-name="ellipse" cx="8" cy="8" r="8"></circle>
                </svg>
              </div>
            </label>
            <label
              class="mt-px cursor-pointer select-none font-light text-gray-700"
              for="pupil"
            >
              Per Pupil Expenditure
            </label>
          </div>
          <div class="inline-flex items-center">
            <label
              class="relative flex cursor-pointer items-center rounded-full p-3 text-indigo-700 border-indigo-700"
              for="alg"
              data-ripple-dark="true"
            >
              <input
                id="alg"
                name="type"
                type="radio"
                class="before:content[''] peer relative h-5 w-5 cursor-pointer appearance-none rounded-full border border-blue-gray-200 text-indigo-700 transition-all before:absolute before:top-2/4 before:left-2/4 before:block before:h-12 before:w-12 before:-translate-y-2/4 before:-translate-x-2/4 before:rounded-full before:bg-blue-gray-500 before:opacity-0 before:transition-opacity checked:border-indigo-700 hover:before:bg-indigo-700 hover:before:opacity-10"
              />
              <div class="pointer-events-none absolute top-2/4 left-2/4 -translate-y-2/4 -translate-x-2/4 text-indigo-700 opacity-0 transition-opacity peer-checked:opacity-100">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-3.5 w-3.5"
                  viewBox="0 0 16 16"
                  fill="currentColor"
                >
                  <circle data-name="ellipse" cx="8" cy="8" r="8"></circle>
                </svg>
              </div>
            </label>
            <label
              class="mt-px cursor-pointer select-none font-light text-gray-700"
              for="alg"
            >
              Algebra Proficiency
            </label>
          </div>
          <div class="inline-flex items-center">
            <label
              class="relative flex cursor-pointer items-center rounded-full p-3 text-fuchsia-800 border-fuchsia-800"
              for="lit"
              data-ripple-dark="true"
            >
              <input
                id="lit"
                name="type"
                type="radio"
                class="before:content[''] peer relative h-5 w-5 cursor-pointer appearance-none rounded-full border border-blue-gray-200 text-fuchsia-800 transition-all before:absolute before:top-2/4 before:left-2/4 before:block before:h-12 before:w-12 before:-translate-y-2/4 before:-translate-x-2/4 before:rounded-full before:bg-blue-gray-500 before:opacity-0 before:transition-opacity checked:border-fuchsia-800 hover:before:bg-fuchsia-800 hover:before:opacity-10"
              />
              <div class="pointer-events-none absolute top-2/4 left-2/4 -translate-y-2/4 -translate-x-2/4 text-fuchsia-800 opacity-0 transition-opacity peer-checked:opacity-100">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-3.5 w-3.5"
                  viewBox="0 0 16 16"
                  fill="currentColor"
                >
                  <circle data-name="ellipse" cx="8" cy="8" r="8"></circle>
                </svg>
              </div>
            </label>
            <label
              class="mt-px cursor-pointer select-none font-light text-gray-700"
              for="lit"
            >
              Literature Proficiency
            </label>
          </div>
          <div class="inline-flex items-center">
            <label
              class="relative flex cursor-pointer items-center rounded-full p-3 text-green-800 border-green-800"
              for="bio"
              data-ripple-dark="true"
            >
              <input
                id="bio"
                name="type"
                type="radio"
                class="before:content[''] peer relative h-5 w-5 cursor-pointer appearance-none rounded-full border border-blue-gray-200 text-green-800 transition-all before:absolute before:top-2/4 before:left-2/4 before:block before:h-12 before:w-12 before:-translate-y-2/4 before:-translate-x-2/4 before:rounded-full before:bg-blue-gray-500 before:opacity-0 before:transition-opacity checked:border-green-800 hover:before:bg-green-800 hover:before:opacity-10"
              />
              <div class="pointer-events-none absolute top-2/4 left-2/4 -translate-y-2/4 -translate-x-2/4 text-green-800 opacity-0 transition-opacity peer-checked:opacity-100">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-3.5 w-3.5"
                  viewBox="0 0 16 16"
                  fill="currentColor"
                >
                  <circle data-name="ellipse" cx="8" cy="8" r="8"></circle>
                </svg>
              </div>
            </label>
            <label
              class="mt-px cursor-pointer select-none font-light text-gray-700"
              for="bio"
            >
              Biology Proficiency
            </label>
          </div>
        </div>
        '''

    return render_template("vis.html",
                           js=js_file,
                           css=css_file,
                           controls=controls,
                           data=data,
                           note=note,
                           attribution=attribution)


@app.route("/scatter")
def get_scatter():
    js_file = url_for('static', filename='scatter/scatter.js')
    css_file = url_for('static', filename='map/andrew.css')
    controls = '''
        <!-- Code for tailwind radio buttons https://www.material-tailwind.com/docs/html/radio-button -->
        <div id="andrew" class="flex gap-10 radio-buttons-container">
          <div <h1>Select a Metric to View</h1></div>
          <div class="inline-flex items-center">
            <label
              class="relative flex cursor-pointer items-center rounded-full p-3 text-indigo-700 border-indigo-700"
              for="alg"
              data-ripple-dark="true"
            >
              <input
                id="alg"
                name="type"
                type="radio"
                class="before:content[''] peer relative h-5 w-5 cursor-pointer appearance-none rounded-full border border-blue-gray-200 text-indigo-700 transition-all before:absolute before:top-2/4 before:left-2/4 before:block before:h-12 before:w-12 before:-translate-y-2/4 before:-translate-x-2/4 before:rounded-full before:bg-blue-gray-500 before:opacity-0 before:transition-opacity checked:border-indigo-700 hover:before:bg-indigo-700 hover:before:opacity-10"
                checked
              />
              <div class="pointer-events-none absolute top-2/4 left-2/4 -translate-y-2/4 -translate-x-2/4 text-indigo-700 opacity-0 transition-opacity peer-checked:opacity-100">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-3.5 w-3.5"
                  viewBox="0 0 16 16"
                  fill="currentColor"
                >
                  <circle data-name="ellipse" cx="8" cy="8" r="8"></circle>
                </svg>
              </div>
            </label>
            <label
              class="mt-px cursor-pointer select-none font-light text-gray-700"
              for="alg"
            >
              Algebra Proficiency
            </label>
          </div>
          <div class="inline-flex items-center">
            <label
              class="relative flex cursor-pointer items-center rounded-full p-3 text-fuchsia-800 border-fuchsia-800"
              for="lit"
              data-ripple-dark="true"
            >
              <input
                id="lit"
                name="type"
                type="radio"
                class="before:content[''] peer relative h-5 w-5 cursor-pointer appearance-none rounded-full border border-blue-gray-200 text-fuchsia-800 transition-all before:absolute before:top-2/4 before:left-2/4 before:block before:h-12 before:w-12 before:-translate-y-2/4 before:-translate-x-2/4 before:rounded-full before:bg-blue-gray-500 before:opacity-0 before:transition-opacity checked:border-fuchsia-800 hover:before:bg-fuchsia-800 hover:before:opacity-10"
              />
              <div class="pointer-events-none absolute top-2/4 left-2/4 -translate-y-2/4 -translate-x-2/4 text-fuchsia-800 opacity-0 transition-opacity peer-checked:opacity-100">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-3.5 w-3.5"
                  viewBox="0 0 16 16"
                  fill="currentColor"
                >
                  <circle data-name="ellipse" cx="8" cy="8" r="8"></circle>
                </svg>
              </div>
            </label>
            <label
              class="mt-px cursor-pointer select-none font-light text-gray-700"
              for="lit"
            >
              Literature Proficiency
            </label>
          </div>
          <div class="inline-flex items-center">
            <label
              class="relative flex cursor-pointer items-center rounded-full p-3 text-green-800 border-green-800"
              for="bio"
              data-ripple-dark="true"
            >
              <input
                id="bio"
                name="type"
                type="radio"
                class="before:content[''] peer relative h-5 w-5 cursor-pointer appearance-none rounded-full border border-blue-gray-200 text-green-800 transition-all before:absolute before:top-2/4 before:left-2/4 before:block before:h-12 before:w-12 before:-translate-y-2/4 before:-translate-x-2/4 before:rounded-full before:bg-blue-gray-500 before:opacity-0 before:transition-opacity checked:border-green-800 hover:before:bg-green-800 hover:before:opacity-10"
              />
              <div class="pointer-events-none absolute top-2/4 left-2/4 -translate-y-2/4 -translate-x-2/4 text-green-800 opacity-0 transition-opacity peer-checked:opacity-100">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-3.5 w-3.5"
                  viewBox="0 0 16 16"
                  fill="currentColor"
                >
                  <circle data-name="ellipse" cx="8" cy="8" r="8"></circle>
                </svg>
              </div>
            </label>
            <label
              class="mt-px cursor-pointer select-none font-light text-gray-700"
              for="bio"
            >
              Biology Proficiency
            </label>
          </div>
        </div>
        '''
    
    note = '''
        <p class="mb-3">Use this map to explore how your school district compares to its neighboring districts and to the state overall.
        <p class="mb-3">Notice the clustering of Per Pupil Expenditure...
        <p class="mb-3">We see generally see the highest per pupil expenditures in Pittsburgh and its surrounding suburbs, in the Philadelphia suburbs but not the city itself, in Indiana and the surrounding districts, and in the fringes of the northeast. We generally see the lowest per pupil expenditures throughout south-central PA and the heart of the northeast.
        <p class="mb-3">However, we can see that academic Proficiency does not map directly onto these expenditure patterns by noticing how the geographical pattern of lowest per pupil expenditures \"disappears\" when viewing rates of Proficiency. One may expect that more money spent would result in better academic outcomes, but we are seeing that may not always be the case.
        <p>For that reason, we want to explore how related expenditure is to academic proficiency in Pennsylvania. Click onto the Scatter plot to explore this question.
           '''

    attribution = '''
        <p>This is 2018-2019 data from the
           <a class="underline"
              href="https://www.education.pa.gov/DataAndReporting/Pages/default.aspx"
               >
               Pennsylvania Department of Education
           </a>.
           The Proficiency data is from the Keystone Exams
           which replaced what many will know as the "PSSAs",
           and are administered to 11th graders
           (with some exceptions for those with special needs).
        '''

    
    return render_template("vis.html",
                           js=js_file,
                           css=css_file,
                           controls=controls,
                           data="",
                           note=note,
                           attribution=attribution)



@app.route("/slope")
def get_slope():
    js_file = url_for('static', filename='slope/slope.js')
    css_file = url_for('static', filename='map/andrew.css')
    controls = ""
    data = "",
    with open('static/slope/compare_ranks.json') as file:
        data = json.load(file)

    note = '''
        <p class="mb-4">The ranked slope chart below shows how school districts across the state rank according to Niche's compared to our value ratio rankings.
        <a class="underline"
            href="https://www.niche.com/about/methodology/best-school-districts/"
            >
            Niche's rankings are calculated according to the metrics outlined on its site.
        </a>
        <p class="mb-4">
            Our value ratio was calculated by taking the average proficiency rate across the three Keystone exams (Algebra I, Biology, and Literature) and comparing it to district per pupil expenditure.
            When non-academic factors such as clubs and activities, sports, and diversity are excluded from calculations, we can see a significant shift in the rankings.
            We also see districts whose average proficiency scores greater than 85% falling to due to their high per pupil expenditure.
            Other districts are achieving the same proficiency rate at a much lower cost.
        <p>
            Select a district from the dropdown menu to see how the two rankings compare.
            To compare your district's performance and per pupil expenditure to others, click on the radar chart.
    '''
    attribution = ''

    return render_template("vis.html",
                           js=js_file,
                           css=css_file,
                           controls=controls,
                           data=data,
                           note=note,
                           attribution=attribution)


@app.route("/radar")
def get_radar():
    js_file = ""
    css_file = ""
    controls = ""
    data = "",
    note = "Notes here"
    attribution = "Attribution here"

    return render_template("vis.html",
                           js=js_file,
                           css=css_file,
                           controls=controls,
                           data=data,
                           note=note,
                           attribution=attribution)


@app.route("/summary")
def get_summary():
    return render_template("summary.html", data="")


# set debugger
if __name__ == "main":
    app.run(debug=True)
