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
                FROM loandata
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
                FROM loandata
                GROUP BY addr_state''')
    results = cur.fetchall()    

    # empty list to append data to
    stats = []

    # loop to append relevant data
    for result in results:
        if result["addr_state"] == state:
            info = {
                "Number of Loans": result["loan_count"],
                "Avg Loan Amount($)": round(result["loan_avg"]),
                "Avg HH Income($)": round(result["inc_avg"]),
                "Avg Interest Rate(%)": round(result["int_avg"],2),
                "Avg DTI(%)": round(result["dti_avg"], 2)
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
                FROM loandata
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
                FROM loandata
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
                FROM loandata
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

# route for returning home owner status for a state
@app.route("/home/<state>")
def homeOwner(state):
    """Return the home owner status for a given state"""

    # query state home ownership
    cur = mysql.connection.cursor()
    cur.execute('''SELECT addr_state,
                home_ownership,
                COUNT(home_ownership) AS owner_count
                FROM loandata
                GROUP BY addr_state, home_ownership''')
    results = cur.fetchall() 

    # empty list to append data to
    owner_status = []
    num_owners = []

    # loop to append relevant data
    for result in results:
        if result["addr_state"] == state:
            owner_status.append(result["home_ownership"])
            num_owners.append(result["owner_count"])

    loan_owners = {
        "owner_status": owner_status,
        "owner_counts": num_owners
    }

    return jsonify(loan_owners)

#################################################
# US Routes
#################################################

# route for returning US statistics
@app.route("/USstats")
def usStats():
    """Return the loan statistics for the US"""

    # query US statistics
    cur = mysql.connection.cursor()
    cur.execute('''SELECT addr_state,
                COUNT(loan_amnt) AS loan_count,
                AVG(loan_amnt) AS loan_avg,
                AVG(annual_inc) AS inc_avg,
                AVG(int_rate) AS int_avg,
                AVG(dti) AS dti_avg
                FROM loandata
                ''')
    results = cur.fetchall()    

    # empty list to append data to
    usstats = []

    # loop to append relevant data
    for result in results:
        info = {
            "Number of Loans": result["loan_count"],
            "Avg Loan Amount($)": round(result["loan_avg"]),
            "Avg HH Income($)": round(result["inc_avg"]),
            "Avg Interest Rate(%)": round(result["int_avg"],2),
            "Avg DTI(%)": round(result["dti_avg"], 2)
        }

        usstats.append(info)

    return jsonify(usstats)

# route for returning loan status data for the US
@app.route("/USstatus")
def usloanStatus():
    """Return the loan status counts for the US"""

    # query US loan status
    cur = mysql.connection.cursor()
    cur.execute('''SELECT addr_state,
                loan_status,
                COUNT(loan_status) AS status_count
                FROM loandata
                GROUP BY loan_status''')
    results = cur.fetchall() 

    # empty list to append data to
    usstatus = []
    uscounts = []

    # loop to append relevant data
    for result in results:
        usstatus.append(result["loan_status"])
        uscounts.append(result["status_count"])

    usloan_counts = {
        "loan_status": usstatus,
        "loan_counts": uscounts
    }

    return jsonify(usloan_counts)

# route for returning loan grade data for the US
@app.route("/USgrades")
def usloanGrades():
    """Return the loan grade counts for the US"""

    # query US loan grades
    cur = mysql.connection.cursor()
    cur.execute('''SELECT addr_state,
                grade,
                COUNT(grade) AS grade_count
                FROM loandata
                GROUP BY grade''')
    results = cur.fetchall() 

    # empty list to append data to
    usgrades = []
    usgrade_counts = []

    # loop to append relevant data
    for result in results:
        usgrades.append(result["grade"])
        usgrade_counts.append(result["grade_count"])

    usstate_grades = {
        "grades": usgrades,
        "grade_counts": usgrade_counts
    }

    return jsonify(usstate_grades)

# route for returning loan year data the US
@app.route("/USyears")
def usloanYears():
    """Return the loan counts per year for the US"""

    # query US loan years
    cur = mysql.connection.cursor()
    cur.execute('''SELECT addr_state,
                issue_y,
                COUNT(issue_y) AS year_count
                FROM loandata
                GROUP BY issue_y''')
    results = cur.fetchall() 

    # empty list to append data to
    usyears = []
    usnum_loans = []

    # loop to append relevant data
    for result in results:
            usyears.append(result["issue_y"])
            usnum_loans.append(result["year_count"])

    usloan_years = {
        "years": usyears,
        "loan_counts": usnum_loans
    }

    return jsonify(usloan_years)

# route for returning home owner status for the US
@app.route("/UShome")
def ushomeOwner():
    """Return the home owner status for the US"""

    # query US home ownership
    cur = mysql.connection.cursor()
    cur.execute('''SELECT addr_state,
                home_ownership,
                COUNT(home_ownership) AS owner_count
                FROM loandata
                GROUP BY home_ownership''')
    results = cur.fetchall() 

    # empty list to append data to
    usowner_status = []
    usnum_owners = []

    # loop to append relevant data
    for result in results:
        usowner_status.append(result["home_ownership"])
        usnum_owners.append(result["owner_count"])

    usloan_owners = {
        "owner_status": usowner_status,
        "owner_counts": usnum_owners
    }

    return jsonify(usloan_owners)

# route for returning Top US States
@app.route("/topstates")
def usTop():
    """Return the Top 10 US States - loan count"""

    # query State loan counts
    cur = mysql.connection.cursor()
    cur.execute('''SELECT addr_state,
                COUNT(loan_amnt) AS loan_count
                FROM loandata
                GROUP BY addr_state
                ORDER BY loan_count DESC
                LIMIT 10''')
    results = cur.fetchall() 

    # empty list to append data to
    usstates = []
    usstate_count = []

    # loop to append relevant data
    for result in results:
            usstates.append(result["addr_state"])
            usstate_count.append(result["loan_count"])

    uscounts = {
        "states": usstates,
        "loan_counts": usstate_count
    }

    return jsonify(uscounts)

if __name__ == "__main__":
    app.run(debug=True)


