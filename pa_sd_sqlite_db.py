## Import dependencies
import sqlite3
from sqlalchemy import create_engine

## Create connection to SQLite database
engine = create_engine("sqlite:///pa_school_district.sqlite3")

## Create a table
engine.execute("CREATE TABLE keystone_school 




