from flask import Flask, render_template, redirect, url_for, session, flash
##from CONFIG import HOST, PORT, DEBUG, APP_SECRET_KEY, DB_LOCATION
##from db_helper import UTC_OFFSET
import psycopg2
import datetime
from ast import literal_eval
from operator import attrgetter
##from picklesession import PickleSessionInterface
import os
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/report_filter')
def report_filter():
    return render_template('report_filter.html')

@app.route('/report_facility')
def report_facility():
    return render_template('report_facility.html')

@app.route('/report_transit')
def report_transit():
    return render_template('report_transit.html')

@app.route('/rest')
def rest():
    return render_template('rest.html')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

