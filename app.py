# dependencies
from flask import (
    Flask, 
    jsonify, 
    render_template, 
    redirect)

import os
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, load_only
from sqlalchemy import create_engine, func, distinct
from flask_sqlalchemy import SQLAlchemy

import numpy as np
import pandas as pd

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/lcdb.sqlite"

db = SQLAlchemy(app)

# Define loan class

class loanData(db.Model):
    __tablename__ = "loans"

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Float)
    loan_amnt = db.Column(db.Float)
    funded_amnt = db.Column(db.Float)
    funded_amnt_inv = db.Column(db.Float)
    term = db.Column(db.String(64))
    int_rate = db.Column(db.String(64))
    installment = db.Column(db.Float)
    grade = db.Column(db.String(64))
    sub_grade = db.Column(db.String(64))
    emp_title = db.Column(db.String(64))
    emp_length = db.Column(db.String(64))
    home_ownership = db.Column(db.String(64))
    annual_inc = db.Column(db.Float)
    verification_status = db.Column(db.String(64))
    issue_d = db.Column(db.String(64))
    issue_y = db.Column(db.String(64))
    loan_status = db.Column(db.String(64))
    pymnt_plan = db.Column(db.String(64))
    url = db.Column(db.String(64))
    desc = db.Column(db.String(64))
    purpose = db.Column(db.String(64))
    title = db.Column(db.String(64))
    zip_code = db.Column(db.String(64))
    addr_state = db.Column(db.String(64))
    dti = db.Column(db.Float)
    delinq_2yrs = db.Column(db.Float)
    earliest_cr_line = db.Column(db.String(64))
    inq_last_6mths = db.Column(db.Float)
    mths_since_last_delinq = db.Column(db.Float)
    mths_since_last_record = db.Column(db.Float)
    open_acc = db.Column(db.Float)
    pub_rec = db.Column(db.Float)
    revol_bal = db.Column(db.Float)
    revol_util = db.Column(db.String(64))
    total_acc = db.Column(db.Float)
    initial_list_status = db.Column(db.String(64))
    out_prncp = db.Column(db.Float)
    out_prncp_inv = db.Column(db.Float)
    total_pymnt = db.Column(db.Float)
    total_pymnt_inv = db.Column(db.Float)
    total_rec_prncp = db.Column(db.Float)
    total_rec_int = db.Column(db.Float)
    total_rec_late_fee = db.Column(db.Float)
    recoveries = db.Column(db.Float)
    collection_recovery_fee = db.Column(db.Float)
    last_pymnt_d = db.Column(db.String(64))
    last_pymnt_amnt = db.Column(db.Float)
    next_pymnt_d = db.Column(db.String(64))

# base route
@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

# route for returning all states
@app.route("/states")
def names():
    """Return a list of states"""

    # results of the query
    results = db.session.query(loanData.addr_state).distinct().order_by(loanData.addr_state)

    # empty list to append data to
    states = []

    # loop to append relevant data
    for result in results:
        states.append(result[0])

    return jsonify(states)

# # route for returning state statistics
@app.route("/stats/<state>")
def stateStats(state):
    """Return the loan statistics for a state."""

    # Selection to query
    sel = [ 
        func.count(loanData.loan_amnt), 
        func.avg(loanData.loan_amnt), 
        func.avg(loanData.annual_inc),
        func.avg(loanData.int_rate), 
        func.avg(loanData.dti)
        ]

    # results of the query
    results = db.session.query(*sel).group_by(loanData.addr_state).having(loanData.addr_state==state)
    # empty list to append data to
    stats = []

    # loop to append relevant data
    for result in results:
        info = {
            "Number of Loans": result[0],
            "Avg Loan Amount": round(result[1],2),
            "Avg HH Income": round(result[2],2),
            "Avg Interest Rate": round(result[3],2),
            "Avg DTI": round(result[4],2)
        }

        stats.append(info)

    return jsonify(stats)

# route for returning loan status data for a state
@app.route("/status/<state>")
def loanStatus(state):
    """Return the loan status counts for a given state"""

    # Selection to query
    sel = [
        loanData.addr_state, 
        loanData.loan_status, 
        func.count(loanData.loan_status)
        ]

    # results of the query
    results = db.session.query(*sel).group_by(loanData.addr_state, loanData.loan_status).having(loanData.addr_state==state)

    # empty list to append data to
    status = []
    counts = []

    # loop to append relevant data
    for result in results:
        status.append(result[1])
        counts.append(result[2])

    loan_counts = {
        "loan_status": status,
        "loan_counts": counts
    }

    return jsonify(loan_counts)

# route for returning loan grade data for a state
@app.route("/grades/<state>")
def loanGrades(state):
    """Return the loan grade counts for a given state"""

    # Selection to query
    sel = [
        loanData.addr_state, 
        loanData.grade, 
        func.count(loanData.grade)
        ]

    # results of the query
    results = db.session.query(*sel).group_by(loanData.addr_state, loanData.grade).having(loanData.addr_state==state)

    # empty list to append data to
    grades = []
    grade_counts = []

    # loop to append relevant data
    for result in results:
        grades.append(result[1])
        grade_counts.append(result[2])

    state_grades = {
        "grades": grades,
        "grade_counts": grade_counts
    }

    return jsonify(state_grades)

# route for returning loan year data for a state
@app.route("/years/<state>")
def loanYears(state):
    """Return the loan counts per year for a given state"""

    # Selection to query
    sel = [
        loanData.addr_state, 
        loanData.issue_y, 
        func.count(loanData.issue_y)
        ]

    # results of the query
    results = db.session.query(*sel).group_by(loanData.addr_state, loanData.issue_y).having(loanData.addr_state==state)

    # empty list to append data to
    years = []
    num_loans = []

    # loop to append relevant data
    for result in results:

        years.append(result[1])
        num_loans.append(result[2])

    loan_years = {
        "years": years,
        "loan_counts": num_loans
    }

    return jsonify(loan_years)

if __name__ == "__main__":
    app.run(debug=True)


