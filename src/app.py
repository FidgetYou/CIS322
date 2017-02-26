from flask import Flask, render_template, redirect, url_for, session, flash, request
from config import dbname, dbhost, dbport
import json
##from db_helper import UTC_OFFSET
import psycopg2
import datetime
from ast import literal_eval
from operator import attrgetter
##from picklesession import PickleSessionInterface
import os
import sys

app = Flask(__name__)

app.secret_key = 'qwertyuiopasdfghjklzxcvbnm'

##session = requests.Session()
conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
cur = conn.cursor()

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'GET':
        return render_template('create_user.html')
    if request.method == 'POST':
        if request.form['uname']:
            print("You've got a name!")
            session['uname'] = request.form['uname']
        else:
            # If there isn't a username in the session
            print("No UserName")
            return render_template('create_user.html')
        
        if request.form['pass'] or request.form['role']:
            print("You've got a password!")
            session['pass'] = request.form['pass']
        else:
            print("No password")
            return render_template('create_user.html')
    
            
        the_username = "'" + request.form['uname'] + "'"
        the_password = "'" + request.form['pass'] + "'"
        the_jobtitle = "'" + request.form['role'] + "'"
        print (the_username)
        
        SQL = "SELECT username FROM user_name WHERE username = %s;"
        one_data = the_username
        cur.execute('SELECT username FROM user_name WHERE username = %s', (one_data,))
        db_row = cur.fetchone()
        print (db_row)

        if db_row is None:
            SQL = "INSERT INTO user_name (username, password, role) VALUES (%s, %s, %s);"
            data = (the_username,the_password,the_jobtitle)
            cur.execute(SQL, data)
            conn.commit()
            print("Added user " + the_username)

            return render_template('added_login.html')
        
        else:
            print("In the database already")
            return render_template('already_user.html')
        

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        if request.form['uname']:
            session['uname'] = request.form['uname']
        else:
            # If there isn't a username in the session
            print("No UserName")
            return render_template('login.html')
        
        if request.form['pass']:
            session['pass'] = request.form['pass']
        else:
            print("No password")
            return render_template('login.html')
    
            
        the_username = "'" + request.form['uname'] + "'"
        the_password = "'" + request.form['pass'] + "'"
        
        SQL = "SELECT username FROM user_name WHERE username = %s;"
        dataIn = (the_username, the_password)
        cur.execute('SELECT username, password FROM user_name WHERE username = %s AND password = %s', (dataIn))
        db_row = cur.fetchone()

        if db_row is None:
            return render_template('wrong_login.html')
        else:
            return render_template('dashboard.html')
        



@app.route('/added_login')
def added_login():
    return render_template('added_login.html')

@app.route('/already_user')
def already_user():
    return render_template('already_user.html')

@app.route('/wrong_login')
def wrong_login():
    return render_template('wrong_login.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')



@app.route('/add_facility', methods=['GET', 'POST'])
def add_facility():
    if request.method == 'GET':
        
        SQL = "SELECT facility_name FROM facility"
        cur.execute(SQL)
        fac = cur.fetchall()
        facility_names = []
        for f in fac:
            a = dict()
            a['facility_name']=f[0]
            facility_names.append(a)
        session['facilities'] = facility_names
        
        return render_template('add_facility.html')


    if request.method == 'POST':
        session['error'] = ""
        if request.form['facil'] and request.form['fcode'] and request.form['finfo']:
            the_flity = "" + request.form['facil'] + ""
            the_fcode = "" + request.form['fcode'] + ""
            the_finfo = "" + request.form['finfo'] + ""
        
            SQL = "SELECT facility_name, facility_code FROM facility WHERE facility_name = %s AND facility_code = %s;"
            data = (the_flity,the_fcode)
            cur.execute(SQL, data)
            db_row = cur.fetchone()
        
            if db_row is None:
                SQL = "INSERT INTO facility (facility_name, facility_code, facility_info) VALUES (%s, %s, %s);"
                data = (the_flity, the_fcode, the_finfo)
                cur.execute(SQL, data)
                conn.commit()

                session['error'] = "" + the_flity + " has been added to the database."
                return render_template('add_facility.html')

            else:
                session['error'] = "The facility " + the_flity + " is already in the database."
                return render_template('add_facility.html')
                      
        else:
            session['error'] = "Please fill in ALL of the boxes."
            return render_template('add_facility.html')



@app.route('/add_asset')
def add_asset():
    
    if request.method == 'GET':

        
        SQL = "SELECT facility_name FROM facility"
        cur.execute(SQL)
        fac = cur.fetchall()
        facility_names = []
        for f in fac:
            a = dict()
            a['facility_name']=f[0]
            facility_names.append(a)
        session['facilities'] = facility_names

        
        SQL = "SELECT asset_tag FROM asset"
        cur.execute(SQL)
        fac = cur.fetchall()
        asset_names = []
        for f in fac:
            a = dict()
            a['asset_tag']=f[0]
            asset_names.append(a)
        session['assets'] = asset_names
        
        return render_template('add_asset.html')


    if request.method == 'POST':
        session['Aerror'] = ""
        if request.form['asset'] and request.form['ainfo']:
            the_asset = "" + request.form['asset'] + ""
            the_ainfo = "" + request.form['ainfo'] + ""
        
            SQL = "SELECT asset_tag FROM asset WHERE asset_tag = %s;"
            Adata = (the_asset)
            cur.execute(SQL, Adata)
            db_row = cur.fetchone()
        
            if db_row is None:
                SQL = "INSERT INTO asset (asset_tag, asset_info) VALUES (%s, %s);"
                Bdata = (the_asset, the_ainfo)
                cur.execute(SQL, Bdata)
                conn.commit()

                SQL = "SELECT asset_pk FROM asset WHERE asset_tag = %s;"
                Adata = (the_asset)
                cur.execute(SQL, Adata)
                db_row1 = cur.fetchone()

                SQL = "SELECT facility_pk FROM facility WHERE facility_name = %s;"
                Adata = (request.form['facil'])
                cur.execute(SQL, Adata)
                db_row2 = cur.fetchone()
        
                SQL = "INSERT INTO asset_at (asset_fk, facility_fk, arrive) VALUES (%s, %s, %s);"
                Cdata = (db_row1, db_row2, request.form['time'])
                cur.execute(SQL, Cdata)
                conn.commit()
                

                session['Aerror'] = "" + the_asset + " has been added to the database."
                return render_template('add_asset.html')

            else:
                session['Aerror'] = "The asset " + the_asset + " is already in the database."
                return render_template('add_asset.html')
                      
        else:
            session['Aerror'] = "Please fill in ALL of the boxes."
            return render_template('add_asset.html')
    



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
