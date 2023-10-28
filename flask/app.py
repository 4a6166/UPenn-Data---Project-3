from flask import Flask, request, render_template, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.sql import func
import json

# connect to DB
engine = create_engine("sqlite:///pa_school_district.db")
Base = automap_base()
Base.prepare(autoload_with=engine)


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
    session = Session(engine)
    view = request.args.get('view', None)

    # return list of dicst with AUN, District, Advanced, Proficient, NumeberScored, and Total (Advanced + Proficient)
    # TODO: move from local scope
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

    # TODO: reused for scatter. Pull out into def.
    if view == "pupil":
        query = session.query(Base.classes.person_spend.AUN,
                              Base.classes.person_spend.LocalPupil,
                              Base.classes.person_spend.StatePupil,
                              Base.classes.person_spend.FedPupil
                              # filted because data for AUN is outlier
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

    session.close()
    return jsonify(results)


# API for scatter plots
@app.route("/api/scatter", methods=['GET'])
def get_scatter_api():
    session = Session(engine)
    view = request.args.get('view', None)
    results = []

    s =''
    if view == 'alg':
        s='keystone_algebra'
    elif view == 'bio':
        s ='keystone_biology'
    elif view == 'lit':
        s='keystone_literature'

    query = session.query(
            func.avg(Base.classes[s].Proficient)
            ).join(Base.classes.person_spend,
                   Base.classes.person_spend.AUN == Base.classes[s].AUN
            ).group_by(Base.classes[s].AUN
            ).order_by(Base.classes.person_spend.AUN.desc())

    for row in query:
        results.append(row[0])

    session.close()
    return jsonify(results)


# Second API for scatter plots
@app.route("/api/pupil")
def get_scatter_pupil():
    session = Session(engine)
    results = []
    query = session.query(Base.classes.person_spend.AUN,
                          Base.classes.person_spend.LocalPupil,
                          Base.classes.person_spend.StatePupil,
                          Base.classes.person_spend.FedPupil
                          # filtered out because data for AUN is incorrect
                          ).filter(Base.classes.person_spend.AUN != "103022253"
                          ).group_by(Base.classes.person_spend.AUN
                          ).order_by(Base.classes.person_spend.AUN.desc())

    for row in query:
        results.append(row[1]+row[2]+row[3])

    session.close()
    return jsonify(results)


# API for slope - Not being used by graph
@app.route("/api/slope", methods=['GET'])
def get_slope_api():
    session = Session(engine)
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

    session.close()
    return jsonify(results)


# API for radar - Not being used by the graphs
@app.route("/api/radar", methods=['GET'])
def get_radar_api():
    return "<p>Nothing here.<p>You feel a comfort in the quiet...<p>as if you never really wanted data for a radar chart at all."


######################################################################
# Serves the webpages
######################################################################
# Makes landing page
@app.route("/")
def home():
    # render the dashboard template
    return render_template("home.html", data="")


# renders the Map page, passing in static downloaded geojson for school boundaries
# but using api to pair it with data from the "/api/map" route
@app.route("/map")
def get_map():
    js_file = url_for('static', filename='map/app.js')
    css_file = url_for('static', filename='map/andrew.css')
    data = ''
    # pass through downloaded geojson for district boundaries
    with open('static/map/Pennsylvania_School_Districts_Boundaries.geojson') as file:
        data = json.load(file)

    # space for comments about the visualization
    note = '''
        <p class="mb-3">Use this map to explore how your school district compares to its neighboring districts and to the state overall.
        <p class="mb-3">Notice the clustering of Per Pupil Expenditure...
        <p class="mb-3">We see generally see the highest per pupil expenditures in Pittsburgh and its surrounding suburbs, in the Philadelphia suburbs but not the city itself, in Indiana and the surrounding districts, and in the fringes of the northeast. We generally see the lowest per pupil expenditures throughout south-central PA and the heart of the northeast.
        <p class="mb-3">However, we can see that academic Proficiency does not map directly onto these expenditure patterns by noticing how the geographical pattern of lowest per pupil expenditures \"disappears\" when viewing rates of Proficiency. One may expect that more money spent would result in better academic outcomes, but we are seeing that may not always be the case.
        <p>For that reason, we want to explore how related expenditure is to academic proficiency in Pennsylvania. Click onto the Scatter plot to explore this question.
           '''

    # space for acknowledgements or footnotes
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

    # controls that load below the visualization
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


# renders the scatter plot, using the "/api/scatter" and "/api/pupil" routes
@app.route("/scatter")
def get_scatter():
    js_file = url_for('static', filename='scatter/scatter.js')

    # controls that load below the visualization
    controls = '''
        <fieldset>
            <div>
                <input type="radio" id="alg" checked></input>
                <label for="alg">Algebra</label>
            </div>
            <div>
                <input type="radio" id="bio"></input>
                <label for="bio">Biology</label>
            </div>
            <div>
                <input type="radio" id="lit"></input>
                <label for="lit">Literature</label>
            </div>
        </fieldset>
    '''

    note = 'Here are scatter plots showing the relationship between expense and performance across three categories.'

    return render_template("vis.html",
                           js=js_file,
                           css="",
                           controls=controls,
                           data="",
                           note=note,
                           attribution="")


# renders the slope chart
# does not use the "/api/slope" route
@app.route("/slope")
def get_slope():
    js_file = url_for('static', filename='slope/slope.js')
    data = "",
    # loads data pregenerated data into a var and passes it through html to js for the vis
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

    return render_template("vis.html",
                           js=js_file,
                           css="",
                           controls="",
                           data=data,
                           note=note,
                           attribution="")


# renders the radar chart and gauge
# does not use the "/api/radar" route
@app.route("/radar")
def get_radar():
    js_file = url_for('static', filename='radar/radar.js')
    css_file = url_for('static', filename='radar/style.css')
    controls = '''
        <div id="peter" class="container">
            <!-- scripts and links from custom html -->
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css"/>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Signika+Negative:wght@300;400;500;600;700&display=swap" rel="stylesheet">

            <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.min.js"></script>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>

            <div class="search-bar">
                <input type="text" id="schoolSearch" placeholder="Search for a school (ex: 'School_Name-District_Name')"/>
                <i class="fa-solid fa-magnifying-glass"></i>
                <i class="fa-solid fa-xmark"></i>
            </div>
            <div class="flex w-full">
                <div class="radar-chart-container w-1/2">
                    <canvas id="myRadarChart"></canvas>
                </div>
                <div class="gauge-chart-container w-1/2">
                    <div id="gaugeChart"></div>
                </div>
            </div>
        </div>
    '''

    data = "",
    # loads data pregenerated data into a var and passes it through html to js for the vis
    with open('static/radar/keystone_expenditure.json') as file:
        data = json.load(file)

    note = '''
        <p class="mb-8">Radar Chart
        <p class="mb-8">Uncover detailed school performance by selecting one school at a time. The radar chart provides a focused look at proficiency in subjects like Algebra, Biology, and Literature.
        <p class="mb-4">Gauge Chart
        <p class="mb-8">Discover the range of per pupil expenditure, from $0 to tens of thousands. It's a glimpse into the financial backdrop shaping our schools.
        <p class="mb-4">Search Bar
        <p class="mb-4">Quickly find specific schools, based on the school name and district name. Type a name, hit enter, and see the charts dynamically update with the information you're interested in.
    '''

    return render_template("vis.html",
                           js=js_file,
                           css=css_file,
                           controls=controls,
                           data=data,
                           note=note,
                           attribution="")


# Unused Summary page
@app.route("/summary")
def get_summary():
    return render_template("summary.html", summary="")


# set debugger
if __name__ == "main":
    app.run(debug=True)
