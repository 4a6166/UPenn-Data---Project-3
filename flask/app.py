from flask import Flask, render_template, jsonify  # Lesson 10-3
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# set up classes
class TempClass(Base):
    __tablename__ = 'temp'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    decimal = Column(Float)


# connect to DB
engine = create_engine("sqlite:///dbname.sqlite")
conn = engine.connect()

# abstract dab
Base.metadata.create_all(engine)

# create session
session = Session(bind=engine)

# # How to query SQL class
# rows = session.query(TempClass).\
#        filter(TempClass.decimal == 1.5).count()
# for row in rows:
#     print(row.name)


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

    # set results var to be passed to js via render_template
    results = ['Populate this with new dics for all the data needed to pass',
               ['nested', 'lists', 'work'],
               {'1. dictionaries': 'Work here too!',
                '2. as do': {'nested': 'dicts'}
                },
               'So, tell me what data you need and I\'ll serve it through a variable',
               'specifically "query_results',
               'and it will pull in for each page'
               ]

    ############################################
    # Run a query!!!!!!!!
    ############################################

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


# set debugger
if __name__ == "main":
    app.run(debug=True)

