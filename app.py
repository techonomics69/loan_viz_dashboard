# dependencies
from flask import (
    Flask, 
    jsonify, 
    render_template, 
    redirect)

import os
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy

import numpy as np
import pandas as pd

from flask_mysqldb import MySQL

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

# Run with heroku env variables
app.config['MYSQL_USER'] = os.environ['USER']
app.config['MYSQL_PASSWORD'] = os.environ['PASSWORD']
app.config['MYSQL_HOST'] = os.environ['HOST']
app.config['MYSQL_DB'] = os.environ['DB']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# base route
@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

# route for returning all states
@app.route("/states")
def names():
    """Return a list of states"""

    # query states
    cur = mysql.connection.cursor()
    cur.execute('''SELECT DISTINCT addr_state 
                FROM loans.loandata
                ORDER BY addr_state''')
    results = cur.fetchall()

    # empty list to append data to
    states = []

    # loop to append relevant data
    for result in results:
        states.append(result["addr_state"])

    return jsonify(states)

# route for returning state statistics
@app.route("/stats/<state>")
def stateStats(state):
    """Return the loan statistics for a state."""

    # query state statistics
    cur = mysql.connection.cursor()
    cur.execute('''SELECT addr_state,
                COUNT(loan_amnt) AS loan_count,
                AVG(loan_amnt) AS loan_avg,
                AVG(annual_inc) AS inc_avg,
                AVG(int_rate) AS int_avg,
                AVG(dti) AS dti_avg
                FROM loans.loandata
                GROUP BY addr_state''')
    results = cur.fetchall()    

    # empty list to append data to
    stats = []

    # loop to append relevant data
    for result in results:
        if result["addr_state"] == state:
            info = {
                "Number of Loans": result["loan_count"],
                "Avg Loan Amount": round(result["loan_avg"]),
                "Avg HH Income": round(result["inc_avg"]),
                "Avg Interest Rate": round(result["int_avg"]),
                "Avg DTI": round(result["dti_avg"])
            }

            stats.append(info)

    return jsonify(stats)

# route for returning loan status data for a state
@app.route("/status/<state>")
def loanStatus(state):
    """Return the loan status counts for a given state"""

    # query state loan status
    cur = mysql.connection.cursor()
    cur.execute('''SELECT addr_state,
                loan_status,
                COUNT(loan_status) AS status_count
                FROM loans.loandata
                GROUP BY addr_state, loan_status''')
    results = cur.fetchall() 

    # empty list to append data to
    status = []
    counts = []

    # loop to append relevant data
    for result in results:
        if result["addr_state"] == state:
            status.append(result["loan_status"])
            counts.append(result["status_count"])

    loan_counts = {
        "loan_status": status,
        "loan_counts": counts
    }

    return jsonify(loan_counts)

# route for returning loan grade data for a state
@app.route("/grades/<state>")
def loanGrades(state):
    """Return the loan grade counts for a given state"""

    # query state loan grades
    cur = mysql.connection.cursor()
    cur.execute('''SELECT addr_state,
                grade,
                COUNT(grade) AS grade_count
                FROM loans.loandata
                GROUP BY addr_state, grade''')
    results = cur.fetchall() 

    # empty list to append data to
    grades = []
    grade_counts = []

    # loop to append relevant data
    for result in results:
        if result["addr_state"] == state:
            grades.append(result["grade"])
            grade_counts.append(result["grade_count"])

    state_grades = {
        "grades": grades,
        "grade_counts": grade_counts
    }

    return jsonify(state_grades)

# route for returning loan year data for a state
@app.route("/years/<state>")
def loanYears(state):
    """Return the loan counts per year for a given state"""

    # query state loan years
    cur = mysql.connection.cursor()
    cur.execute('''SELECT addr_state,
                issue_y,
                COUNT(issue_y) AS year_count
                FROM loans.loandata
                GROUP BY addr_state, issue_y''')
    results = cur.fetchall() 

    # empty list to append data to
    years = []
    num_loans = []

    # loop to append relevant data
    for result in results:
        if result["addr_state"] == state:
            years.append(result["issue_y"])
            num_loans.append(result["year_count"])

    loan_years = {
        "years": years,
        "loan_counts": num_loans
    }

    return jsonify(loan_years)

if __name__ == "__main__":
    app.run(debug=True)


