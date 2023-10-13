# Alternate file. Attempt to use flask_sqlalchemy python module

from flask import Flask, render_template  # Lesson 10-3
# install Flask-SQLAlchemy in conda dev environment
# conda install -c conda-forge flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

# set up DB via SQLAlchemy
db = SQLAlchemy()

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
    # render the dashboard template
    return render_template("home.html")


# set debugger
if __name__ == "main":
    app.run(debug=True)
