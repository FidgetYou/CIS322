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
                return redirect(url_for('add_facility'))
            
            else:
                session['error'] = "The facility " + the_flity + " is already in the database."
                return render_template('add_facility.html')
                      
        else:
            session['error'] = "Please fill in ALL of the boxes."
            return render_template('add_facility.html')



@app.route('/add_asset', methods=['GET', 'POST'])
def add_asset():
    
    if request.method == 'GET':

        
        SQL = "SELECT facility_name FROM facility"
        cur.execute(SQL)
        fac = cur.fetchall()
        facility_name = []
        for f in fac:
            a = dict()
            a['facility_name']=f[0]
            facility_name.append(a)
        session['facilities'] = facility_name

        ##print (session['facilities'])
        
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
            the_facil = "" + request.form['facilitymenu'] + ""
            the_times = datetime.datetime.strptime(request.form['time'], '%Y-%m-%dT%H:%M') 


            SQL = "SELECT asset_tag FROM asset WHERE asset_tag = %s;"
            Adata = the_asset
            cur.execute(SQL, (Adata,))
            db_row = cur.fetchone()
        
            if db_row is None:
                SQL = "INSERT INTO asset (asset_tag, asset_info) VALUES (%s, %s);"
                Bdata = (the_asset, the_ainfo)
                cur.execute(SQL, Bdata)
                conn.commit()

                SQL = "SELECT asset_pk FROM asset WHERE asset_tag = %s;"
                Adata = the_asset
                cur.execute(SQL, (Adata,))
                db_row1 = cur.fetchone()
                #print (db_row1)

                SQL = "SELECT facility_pk FROM facility WHERE facility_name = %s;"
                Adata = the_facil
                cur.execute(SQL, (Adata,))
                db_row2 = cur.fetchone()
                #print (db_row2)        

                SQL = "INSERT INTO asset_at (asset_fk, facility_fk, arrive) VALUES (%s, %s, %s);"
                Cdata = (db_row1, db_row2, the_times)
                cur.execute(SQL, Cdata)
                conn.commit()
                

                session['Aerror'] = "" + the_asset + " has been added to the database."
                return redirect(url_for('add_asset'))

            else:
                session['Aerror'] = "The asset " + the_asset + " is already in the database."
                return render_template('add_asset.html')
                      
        else:
            session['Aerror'] = "Please fill in ALL of the boxes."
            return render_template('add_asset.html')
    

@app.route('/dispose_asset', methods=['GET', 'POST'])
def dispose_asset():
    
    if request.method == 'GET':
        
        SQL = "SELECT asset_tag FROM asset"
        cur.execute(SQL)
        fac = cur.fetchall()
        asset_names = []
        for f in fac:
            a = dict()
            a['asset_tag']=f[0]
            asset_names.append(a)
        session['assets'] = asset_names
        
        SQL = "SELECT role FROM user_name WHERE username = %s AND role = %s;"
        data = (session['uname'], 'Logistics Officer')
        cur.execute(SQL, data)
        db_row = cur.fetchone()
        
        if db_row is None:
            session['Derror'] = "" + session['uname'] + ": is not authorized to delete assets."
            return redirect(url_for('dispose_asset'))
        else:
            return render_template('dispose_asset.html')


    if request.method == 'POST':
        session['Derror'] = ""
        
        SQL = "SELECT role FROM user_name WHERE username = %s AND role = %s;"
        data = (session['uname'], 'Logistics Officer')
        cur.execute(SQL, data)
        db_row = cur.fetchone()
        
        if db_row is None:
            session['Derror'] = "" + session['uname'] + ": is not authorized to delete assets."
            return redirect(url_for('dispose_asset'))
        
        if request.form['asset'] and request.form['time']:
            the_asset = "" + request.form['asset'] + ""
            the_times = datetime.datetime.strptime(request.form['time'], '%Y-%m-%dT%H:%M') 


            SQL = "SELECT asset_tag FROM asset WHERE asset_tag = %s;"
            Adata = the_asset
            cur.execute(SQL, (Adata,))
            db_row = cur.fetchone()
        
            if db_row is not None:

                SQL = "SELECT asset.asset_tag asset_at.disposed FROM asset JOIN asset_at ON asset.asset_pk=asset_at.asset_fk WHERE asset_tag = %s AND disposed = 'false';"
                Adata = the_asset
                cur.execute(SQL, (Adata,))
                db_row1 = cur.fetchone()
                print (db_row1)
                
                if db_row1 is None:
                    SQL = "INSERT INTO asset_at (depart, disposed) VALUES (%s, true);"
                    Adata = the_times
                    cur.execute(SQL, (Adata,))
                    conn.commit()

                    session['Derror'] = "" + the_asset + " has been deleted from the database."
                    return redirect(url_for('dashboard'))
                else:
                    session['Derror'] = "The asset " + the_asset + " has already been disposed of."
                    return render_template('dispose_asset.html')
            else:
                session['Derror'] = "The asset " + the_asset + " is not in the database."
                return render_template('dispose_asset.html')
                      
        else:
            session['Derror'] = "Please fill in ALL of the boxes."
            return render_template('dispose_asset.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
