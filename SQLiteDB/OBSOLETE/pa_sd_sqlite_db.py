## Import dependencies
import sqlite3
from sqlalchemy import create_engine
import openpyxl

conn = sqlite3.connect("pa_school_district.db")

c = conn.cursor()

create_table_statement = ("""CREATE TABLE keystone_state (
          subject TEXT PRIMARY KEY,
          group TEXT,
          grade INTEGER,
          number_scored INTEGER,
          percent_below_basic REAL,
          percent_basic REAL,
          percent_proficient REAL,
          percent_advanced REAL,
          percent_advanced_proficient REAL
);""")

c.execute(create_table_statement)

conn.commit()

conn.close()

#wb = openpyxl.load_workbook("2019 Keystone Exams School Level Data_db.xlsx")

#ws = wb.active

#column_headers = [cell.value for cell in ws.rows[0]]

#insert_statement = "INSERT INTO table_name ({}) VALUES ({})".format(",".join(column_headers), ",".join(["?" for i in range(len(column_headers))]))
