from flask import Flask, render_template, redirect, url_for, session, flash, request
from config import dbname, dbhost, dbport
import json
##from db_helper import UTC_OFFSET
import psycopg2
import datetime
import string
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
        SQL = "SELECT role FROM role"
        cur.execute(SQL)
        rol = cur.fetchall()
        roles = []
        for f in rol:
            a = dict()
            a['role']=f[0]
            roles.append(a)
        session['roles'] = roles
        print ("roles session = ")
        print (session['roles'])
        

        return render_template('create_user.html')
    if request.method == 'POST':
        if request.form['uname']:
            #print("You've got a name!")
            session['uname'] = request.form['uname']
        else:
            # If there isn't a username in the session
            session['error'] = "No UserName"
            return render_template('create_user.html')
        
        if request.form['pass'] or request.form['role']:
            #print("You've got a password!")
            session['pass'] = request.form['pass']
        else:
            session['error'] = "No password"
            return render_template('create_user.html')
    
            
        the_username = "" + request.form['uname'] + ""
        the_password = "" + request.form['pass'] + ""
        the_jobtitle = "" + request.form['role_menu'] + ""
        #print (the_username)
        
        SQL = "SELECT username FROM user_name WHERE username = %s;"
        one_data = the_username
        cur.execute('SELECT username FROM user_name WHERE username = %s', (one_data,))
        db_row = cur.fetchone()
        #print (db_row)

        if db_row is None:
            try:
                SQL = "SELECT role_pk FROM role WHERE role = %s;"
                one_data = the_jobtitle
                cur.execute(SQL, (one_data,))
                role_fk = cur.fetchone()
                #print (db_row)
            except:
                session['error'] = "" + the_jobtitle + " is invalid."
                return render_template('login.html')
        
            SQL = "INSERT INTO user_name (username, password, role_fk) VALUES (%s, %s, %s);"
            data = (the_username,the_password,role_fk)
            cur.execute(SQL, data)
            conn.commit()
            print("Added user " + the_username)
            session['error'] = "" + the_username + " has been added"
            return render_template('login.html')
        
        else:
            session['error'] = "" + the_username + " has already been taken."
            return render_template('create_user.html')
        

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'GET':
        session['uname'] = ""
        session['pass'] = ""
        session['role'] = ""
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
    
            
        the_username = "" + request.form['uname'] + ""
        the_password = "" + request.form['pass'] + ""
        
        SQL = "SELECT username FROM user_name WHERE username = %s;"
        dataIn = (the_username, the_password)
        cur.execute('SELECT username, password FROM user_name WHERE username = %s AND password = %s', (dataIn))
        db_row = cur.fetchone()

        if db_row is None:
            session['error'] = "That " + the_username + "/" + the_password + " combonation is invalid."
            return render_template('login.html')
        else:
            SQL = "SELECT username FROM user_name WHERE username = %s;"
            dataIn = (the_username, )
            cur.execute('SELECT role.role FROM role, user_name WHERE user_name.username = %s AND user_name.role_fk = role.role_pk', (dataIn))
            db_row = cur.fetchone()
            ##session['role'] = filter(str.db_row, string.printable)
            session['role'] = "".join(filter(lambda x:x in string.printable, db_row))
            session['error'] = ""
            return render_template('dashboard.html')
        



@app.route('/asset_report')
def asset_report():
    return render_template('asset_report.html')

@app.route('/transfer_report')
def transfer_report():
    return render_template('transfer_report.html')

@app.route('/transfer_req', methods=['GET', 'POST'])
def transfer_req():
    logisticsOfficer = "Logistics Officer"
    if session['role'] != logisticsOfficer:
        session['error'] = "You can't go in there! Why, you're not a Logistics Officer."
        return render_template('dashboard.html')
    
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
        
        SQL = "SELECT asset.asset_tag, facility.facility_name FROM asset, asset_at, facility WHERE asset.asset_pk = asset_at.asset_fk AND facility.facility_pk = asset_at.facility_pk AND asset_at.disposed = false"
        cur.execute(SQL)
        ac = cur.fetchone()

        asset_name = []
        for f in ac:
            b = dict()
            b['asset_name']=f[0]
            b['facility_name']=f[1]
            asset_trsf.append(b)

        session['assets_transfer'] = asset_trsf
        ##session['facility_transfer'] = facil_trsf
        print ("session asset = ")
        print (session['assets_transfer'])
        
        ##SQL = "SELECT asset.asset_tag, facility.facility_name FROM asset, asset_at, facility WHERE asset.asset_pk = asset_at.asset_fk AND facility.facility_pk = asset_at.facility_pk AND asset_at.disposed = false"
        ##cur.execute(SQL)
        ##ac = cur.fetchone()
        ##session['current_facility'] = ac
        
        return render_template('transfer_req.html')
    
    if request.method == 'POST':
        session['error'] = ""
        if request.form['asset_menu'] and request.form['facility_menu']:
            SQL = "SELECT facility_name FROM facility, asset, asset_at WHERE asset.asset_tag = %s AND asset.asset_pk = asset_at.asset_fk AND asset_at.facility_fk = facility.facility_pk;"
            Adata = the_asset
            cur.execute(SQL, (Adata,))
            the_dest = cur.fetchone()
            
            the_asset = "" + request.form['asset_menu'] + ""
            the_facil = "" + request.form['facility_menu'] + ""
            the_users = session['uname']
            
            SQL = "SELECT facility_name FROM facility WHERE facility_name = %s;"
            Adata = the_facil
            cur.execute(SQL, (Adata,))
            db_row = cur.fetchone()
        
            if db_row is None:
                session['error'] = "That destination does not exist."
                return render_template('transfer_req.html')
            
            SQL = "SELECT asset_tag FROM asset WHERE asset_tag = %s;"
            Adata = the_asset
            cur.execute(SQL, (Adata,))
            db_row = cur.fetchone()
        
            if db_row is None:
                session['error'] = "That asset does not exist."
                return render_template('transfer_req.html')
            
            SQL = "SELECT asset.asset_tag FROM asset, asset_at WHERE asset.asset_pk = asset_at.asset_fk AND asset_at.disposed = false AND asset_at.in_transit = false AND asset.asset_tag = %s;"
            Adata = the_asset
            cur.execute(SQL, (Adata,))
            db_row = cur.fetchone()
        
            if db_row is None:
                session['error'] = "That is not at that facility."
                return render_template('transfer_req.html')
            
            SQL = "SELECT facility.facility_name FROM asset, asset_at, facility WHERE asset.asset_pk = asset_at.asset_fk AND facility.facility_pk = asset_at.facility_fk AND asset_at.disposed = false AND asset_at.in_transit = false AND facility.facility_name = %s;"
            Adata = the_facil
            cur.execute(SQL, (Adata,))
            db_row = cur.fetchone()
        
            if db_row is not None:
                session['error'] = "The asset is already at that facility."
                return render_template('transfer_req.html')
            
            SQL = "INSERT INTO requests (asset_fk, requester, source_fac, destination_fac) VALUES (%s, %s, %s, %s);"
            fourdata = (the_times, the_users, the_dest, the_facil)
            cur.execute(SQL, fourdata)
            conn.commit()
                    
            return redirect(url_for('transfer_req'))
        else:
            session['error'] = "Please fill in ALL of the boxes."
            return render_template('transfer_req.html')
    
@app.route('/logout')
def logout():
    return render_template('logout.html')


@app.route('/do_work', methods=['GET'])
def do_work():
    logisticsOfficer = "Logistics Officer"
    if session['role'] == logisticsOfficer:
        return render_template('transfer_req.html')
    else:
        return render_template('transfer_req.html')
    
    return render_template('dashboard.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    logisticsOfficer = "Logistics Officer"
    if session['role'] == logisticsOfficer:
        SQL = "SELECT asset.asset_tag FROM asset, transit WHERE transit.asset_fk = asset.asset_pk AND (transit.load_time = null OR transit.unload_time = null"
    else:
        SQL = "SELECT asset.asset_tag FROM asset, requests WHERE requests.asset_fk = asset.asset_pk AND requests.approved = false AND requests.rejected = false "
    cur.execute(SQL)
    fac = cur.fetchall()
    facility_name = []
    for f in fac:
        a = dict()
        a['work']=f[0]
        facility_name.append(a)
    session['works'] = facility_name

    ##print (session['facilities'])
        

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
        ##print ("facility session = ")
        ##print (session['facilities'])
        
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
        ac = cur.fetchall()

        asset_name = []
        for f in ac:
            b = dict()
            b['asset_tag']=f[0]
            asset_name.append(b)

        session['assets'] = asset_name
        ##print ("session asset = ")
        ##print (session['assets'])
        
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
        
        SQL = "SELECT role.role FROM role, user_name WHERE user_name.username = %s AND role.role = %s;"
        data = (session['uname'], 'Logistics Officer')
        cur.execute(SQL, data)
        db_row = cur.fetchone()
        
        if db_row is None:
            session['Derror'] = "" + session['uname'] + ": is not authorized to delete assets."
            return render_template('dispose_asset.html')
        else:
            return render_template('dispose_asset.html')


    if request.method == 'POST':
        session['Derror'] = ""
        
        SQL = "SELECT role.role FROM role, user_name WHERE user_name.username = %s AND role.role = %s;"
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

                SQL = "SELECT asset.asset_tag, asset_at.disposed FROM asset, asset_at WHERE asset.asset_pk=asset_at.asset_fk AND asset.asset_tag = %s AND asset_at.disposed = 'false';"
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
