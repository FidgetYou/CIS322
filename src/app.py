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

@app.route('/activate_user', methods=['POST'])
def activate_user():
    
    error_str = " "
    #the_data = dict()
    
    if request.method=='POST':
        #the_req = json.loads(request.form['arguments'])

        the_username = request.form['name']
        the_password = request.form['pass']
            
        if request.form['role']:
            if request.form['role'] == 'logofc':
                the_jobtitle = "Logistics Officer"
            elif request.form['role'] == 'facofc':
                the_jobtitle = "Facilities Officer"
            else:
                error_str = "That's not a real job"
        else:
             error_str = "No Job"
            
        #the_username = "" + request.form['uname'] + ""
        #the_password = "" + request.form['pass'] + ""
        #the_jobtitle = "" + request.form['role_menu'] + ""
        #print (the_username)
        if error_str == " ":
        
            SQL = "SELECT username FROM user_name WHERE username = %s;"
            one_data = the_username
            cur.execute('SELECT username FROM user_name WHERE username = %s', (one_data,))
            db_row = cur.fetchone()
            #print (db_row)

        
            try:
                SQL = "SELECT role_pk FROM role WHERE role = %s;"
                one_data = the_jobtitle
                cur.execute(SQL, (one_data,))
                role_fk = cur.fetchone()
                #print (db_row)
            except:
                error_str = "" + the_jobtitle + " is invalid."
                #return render_template('login.html')
            
            if db_row is None and error_str == " ":
        
                SQL = "INSERT INTO user_name (username, password, role_fk, active) VALUES (%s, %s, %s, true);"
                data = (the_username,the_password,role_fk)
                cur.execute(SQL, data)
                conn.commit()
                print("Added user " + the_username)
                error_str = "" + the_username + " has been added."
                #return render_template('login.html')
        
            elif error_str == " ":
                SQL = "UPDATE user_name SET active = true, password = %s WHERE username = %s;"
                Bdata = (the_password, the_username)
                cur.execute(SQL, Bdata)
                conn.commit()
                error_str = "" + the_username + "'s password has been updated."
                #return render_template('create_user.html')
            else:
                print(error_str)
        
        #the_data['error'] = error_str
        #data = json.dumps(dat)
        return error_str
    
    
@app.route('/revoke_user', methods=['POST'])
def revoke_user():
    
    error_str = " "
    #the_data = dict()
    
    if request.method=='POST':
        #the_req = json.loads(request.form['arguments'])

        the_username = request.form['name']

        if error_str == " ":
        
            SQL = "SELECT username FROM user_name WHERE username = %s;"
            one_data = the_username
            cur.execute('SELECT username FROM user_name WHERE username = %s', (one_data,))
            db_row = cur.fetchone()
            #print (db_row)

            if db_row is not None:
                SQL = "UPDATE user_name SET active = false WHERE username = %s;"
                Bdata = (the_username, )
                cur.execute(SQL, Bdata)
                conn.commit()
                error_str = "" + the_username + "'s access has been removed."
                #return render_template('create_user.html')
            else:
                error_str = "" + the_username + "is not an employee."
        
        return error_str
    
    

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    return render_template('dashboard.html')
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
        #if request.method=='POST' and 'arguments' in request.form:
            #req = json.loads(request.form['arguments'])
        if request.form['uname']:
            session['uname'] = request.form['uname']
        else:
            session['error'] = "No UserName"
            return render_template('create_user.html')
        
        if request.form['pass'] or request.form['role']:
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

        
        try:
            SQL = "SELECT role_pk FROM role WHERE role = %s;"
            one_data = the_jobtitle
            cur.execute(SQL, (one_data,))
            role_fk = cur.fetchone()
            #print (db_row)
        except:
            session['error'] = "" + the_jobtitle + " is invalid."
            return render_template('login.html')
            
        if db_row is None:
        
            SQL = "INSERT INTO user_name (username, password, role_fk, active) VALUES (%s, %s, %s, true);"
            data = (the_username,the_password,role_fk)
            cur.execute(SQL, data)
            conn.commit()
            print("Added user " + the_username)
            session['error'] = "" + the_username + " has been added"
            return render_template('login.html')
        
        else:
            SQL = "UPDATE user_name SET active = true, password = %s WHERE username = %s;"
            Bdata = (the_password, the_username)
            cur.execute(SQL, Bdata)
            conn.commit()
            #session['error'] = "" + the_username + " has already been taken."
            #return render_template('create_user.html')
        

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    session['uname'] = ""
    session['pass'] = ""
    session['role'] = ""
    
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
    
            
        the_username = "" + request.form['uname'] + ""
        the_password = "" + request.form['pass'] + ""
        
        #SQL = "SELECT username FROM user_name WHERE username = %s;"
        #dataIn = (the_username, the_password)
        #cur.execute('SELECT username, password FROM user_name WHERE username = %s AND password = %s', (dataIn))
        #db_row = cur.fetchone()

        SQL = "SELECT username, password FROM user_name WHERE username = %s AND password = %s AND active = true;"
        dataIn = (the_username, the_password)
        cur.execute(SQL, dataIn)
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
            ##session['role'] = "".join(filter(lambda x:x in string.printable, db_row))
            session['role'] = db_row[0]
            session['error'] = ""
            return redirect(url_for('dashboard'))
        



@app.route('/asset_report')
def asset_report():
    return render_template('asset_report.html')

@app.route('/transfer_report')
def transfer_report():
    return render_template('transfer_report.html')

@app.route('/transfer_req', methods=['GET', 'POST'])
def transfer_req():
    logisticsOfficer = "Logistics Officer"
    try:
        if session['role'] != logisticsOfficer:
            session['error'] = "You can't go in there! Why, you're not a Logistics Officer."
            return render_template('dashboard.html')
    except:
        session['error'] = "You have not logged in yet."
        return render_template('login.html')
    
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
        
        SQL = "SELECT asset.asset_tag, facility.facility_name FROM asset, asset_at, facility WHERE asset.asset_pk = asset_at.asset_fk AND facility.facility_pk = asset_at.facility_fk AND asset_at.disposed = false"
        cur.execute(SQL)
        ac = cur.fetchall()
        print ("what does a query return = ")
        print (ac)
        
        asset_trsf = []
        facil_trsf = []
        ##ass = False
        for f in ac:
            ##ass = not ass
            ##if ass:
            b = dict()
            b['asset_name']=f[0]
            #print ("add asset = ")
            #print (f[0])
            #print ("what is b = ")
            #print (b)
            #asset_trsf.append(b)
            #else:
            #c = dict()
            b['facility_name']=f[1]
            #print ("add facility = ")
            ##print (f[1])
            #print ("what is b = ")
            #print (b)
            asset_trsf.append(b)
            #facil_trsf.append(c)

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
        the_asset = "" + request.form['asset_menu'] + ""
        the_facil = "" + request.form['facility_menu'] + ""
        the_users = session['uname']
        
        if request.form['asset_menu'] and request.form['facility_menu']:
            SQL = "SELECT facility_name FROM facility, asset, asset_at WHERE asset.asset_tag = %s AND asset.asset_pk = asset_at.asset_fk AND asset_at.facility_fk = facility.facility_pk;"
            Adata = the_asset
            cur.execute(SQL, (Adata,))
            the_dest = cur.fetchone()
            
            
            SQL = "SELECT facility_name FROM facility WHERE facility_name = %s;"
            Adata = the_facil
            cur.execute(SQL, (Adata,))
            test1 = cur.fetchone()
        
            if test1 is None:
                session['error'] = "That destination does not exist."
                return render_template('transfer_req.html')
            
            SQL = "SELECT asset.asset_tag FROM asset, asset_at WHERE asset.asset_tag = %s AND asset_at.disposed = false;"
            Adata = the_asset
            cur.execute(SQL, (Adata,))
            test2 = cur.fetchone()
        
            if test2 is None:
                session['error'] = "That asset has been disposed of."
                return render_template('transfer_req.html')
            
            SQL = "SELECT asset.asset_tag FROM asset, requests WHERE asset.asset_tag = %s AND requests.asset_fk = asset.asset_pk;"
            Adata = the_asset
            cur.execute(SQL, (Adata,))
            test3 = cur.fetchone()
        
            if test3 is not None:
                session['error'] = "This asset has already been requested for transfer."
                return render_template('transfer_req.html')
            
            SQL = "SELECT asset.asset_tag FROM asset, asset_at WHERE asset.asset_pk = asset_at.asset_fk AND asset_at.disposed = false AND asset_at.in_transit = false AND asset.asset_tag = %s;"
            Adata = the_asset
            cur.execute(SQL, (Adata,))
            test4 = cur.fetchone()
        
            if test4 is None:
                session['error'] = "That is not at that facility."
                return render_template('transfer_req.html')
            
            SQL = "SELECT facility.facility_name FROM asset, asset_at, facility WHERE asset.asset_pk = asset_at.asset_fk AND facility.facility_pk = asset_at.facility_fk AND asset_at.disposed = false AND asset_at.in_transit = false AND facility.facility_name = %s AND asset.asset_tag = %s;"
            Bdata = (the_facil, the_asset)
            cur.execute(SQL, Bdata)
            test5 = cur.fetchone()
            #print(test5)
        
            if test5 is not None:
                session['error'] = "The asset is already at that facility."
                return render_template('transfer_req.html')
            
            
            ## Insert all the Foreign Keys into Request table.
            SQL = "SELECT facility_pk FROM facility WHERE facility_name = %s;"
            Adata = the_facil
            cur.execute(SQL, (Adata,))
            dest_fac_fk = cur.fetchone()
            
            SQL = "SELECT user_pk FROM user_name WHERE username = %s;"
            Adata = the_users
            cur.execute(SQL, (Adata,))
            user_fk = cur.fetchone()
            
            SQL = "SELECT facility.facility_pk FROM facility, asset, asset_at WHERE asset.asset_tag = %s AND asset.asset_pk = asset_at.asset_fk AND asset_at.facility_fk = facility.facility_pk;"
            Bdata = (the_asset, )
            cur.execute(SQL, Bdata)
            sour_fac_fk = cur.fetchone()
            
            SQL = "SELECT asset_pk FROM asset WHERE asset_tag = %s;"
            Adata = the_asset
            cur.execute(SQL, (Adata,))
            ass_fk = cur.fetchone()
            
            #req_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M").isoformat()
            
            now = datetime.datetime.now()
            print(now)
            str_now = now.date().isoformat()
            print (str_now)

            SQL = "INSERT INTO requests (asset_fk, requester, source_fac, destination_fac, request_time) VALUES (%s, %s, %s, %s, %s);"
            fourdata = (ass_fk, user_fk, sour_fac_fk, dest_fac_fk, str_now)
            cur.execute(SQL, fourdata)
            conn.commit()
                    
            session['error'] = "The transfer request has been created."
            return redirect(url_for('transfer_req'))
        else:
            session['error'] = "Please fill in ALL of the boxes."
            return render_template('transfer_req.html')
    


@app.route('/approve_req', methods=['GET', 'POST'])
def approve_req():
    facilitiesOfficer = "Facilities Officer"
    try:
        if session['role'] != facilitiesOfficer:
            session['error'] = "You can't go in there! Why, you're not a Facilities Officer."
            return render_template('dashboard.html')
    except:
        session['error'] = "You haven't logged in yet."
        return render_template('login.html')
    
    
    if request.method == 'GET':
        the_users = session['uname']
        the_id = session['id']
        SQL = "SELECT requester FROM requests WHERE request_pk = %s AND approved = false AND rejected = false"
        Adata = the_id
        cur.execute(SQL, (Adata,))
        db_row = cur.fetchone()
        
        if db_row is None:
            session['error'] = "This is an invalid request."
            return render_template('approve_req.html')
        
        
        SQL = "SELECT requester FROM requests WHERE request_pk = %s AND approved = true"
        Adata = the_id
        cur.execute(SQL, (Adata,))
        db_row = cur.fetchone()
        
        if db_row is not None:
            session['error'] = "This is an invalid request."
            return render_template('approve_req.html')
        
        SQL = "SELECT requester FROM requests WHERE request_pk = %s AND rejected = true"
        Adata = the_id
        cur.execute(SQL, (Adata,))
        db_row = cur.fetchone()
        
        if db_row is not None:
            session['error'] = "This is an invalid request."
            return render_template('approve_req.html')
        
        
        ## Building the request line of text.
        SQL = "SELECT user_name.username, asset.asset_tag, facility.facility_name, requests.request_time FROM asset, requests, facility, user_name WHERE requests.asset_fk = asset.asset_pk AND requests.requester = user_name.user_pk AND requests.source_fac = facility.facility_pk AND requests.request_pk = %s "
        Adata = the_id
        cur.execute(SQL, (Adata,))
        ac = cur.fetchone()
        #print ("what does a query return = ")
        #print (ac)

        rTime = str(ac[3])
        request_txt = "" + ac[0] + " suggested at " + rTime + " that " + ac[1] + " be moved from " + ac[2] + " to "
        
        # With two facility names, I can't seem to get all of the results into one query.
        SQL = "SELECT facility.facility_name FROM requests, facility WHERE requests.destination_fac = facility.facility_pk AND requests.request_pk = %s "
        Adata = the_id
        cur.execute(SQL, (Adata,))
        ac = cur.fetchone()
        #print ("what does a query return = ")
        #print (ac)
        
        request_txt = request_txt + "" + ac[0] + "."
        session['request_text'] = request_txt
        
        return render_template('approve_req.html')
    
    if request.method == 'POST':
        session['error'] = ""
        the_users = session['uname']
        the_id = session['id']
        #if request.form['facil'] and request.form['fcode'] and request.form['finfo']:
        if request.form['submit'] == 'Deny':
            SQL = "UPDATE requests SET rejected = true WHERE request_pk = %s;"
            Adata = the_id
            cur.execute(SQL, (Adata,))
            conn.commit()
            
            session['error'] = "Okay, we won't move that."
            return render_template('dashboard.html')
        
        if request.form['submit'] == 'Approve':
            #app_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M").isoformat()
            now = datetime.datetime.now()
            print(now)
            app_time = now.date().isoformat()
            print (app_time)
            
            SQL = "SELECT user_pk FROM user_name WHERE username = %s "
            Adata = the_users
            cur.execute(SQL, (Adata,))
            ac = cur.fetchone()
            user_fk = ac[0]
            print ("approved?")
            SQL = "UPDATE requests SET approved = true, approve_time = %s, approver = %s WHERE requests.request_pk = %s;"
            Bdata = (app_time, user_fk, the_id)
            cur.execute(SQL, Bdata)
            conn.commit()
            
            SQL = "INSERT INTO transit (asset_fk, source_fac, destination_fac) SELECT asset_fk, source_fac, destination_fac FROM requests WHERE requests.request_pk = %s;"
            Bdata = (the_id, )
            cur.execute(SQL, Bdata)
            conn.commit()
            
            return render_template('dashboard.html')
        
        return render_template('approve_req.html')
        
@app.route('/logout')
def logout():
    return render_template('login.html')

@app.route('/update_transit', methods=['GET', 'POST'])
def update_transit():
    logisticsOfficer = "Logistics Officer"
    try:
        if session['role'] != logisticsOfficer:
            session['error'] = "You can't go in there! Why, you're not a Logistics Officer."
            return render_template('dashboard.html')
    except:
        session['error'] = "You haven't logged in yet."
        return render_template('login.html')
    
    if request.method == 'GET':
        the_users = session['uname']
        the_id = session['id']
        SQL = "SELECT asset_fk FROM transit WHERE transit_pk = %s AND unload_time = null "
        Adata = the_id
        cur.execute(SQL, (Adata,))
        db_row = cur.fetchone()
        
        if db_row is None:
            session['error'] = "This is an invalid request."
            return render_template('update_transit.html')
        
        
        SQL = "SELECT asset.asset_tag FROM asset, asset_at, transit WHERE transit.transit_pk = %s AND asset.asset_pk = transit.asset_fk AND asset.asset_pk = asset_at.asset_fk AND asset_at.in_transit = false AND asset_at.disposed = false "
        Adata = the_id
        cur.execute(SQL, (Adata,))
        db_row = cur.fetchone()
        
        if db_row is None:
            session['error'] = "This is an invalid request."
            return render_template('approve_req.html')
        
        
        SQL = "SELECT user_name.username, asset.asset_tag, facility.facility_name, requests.approve_time FROM asset, requests, facility, user_name WHERE requests.asset_fk = asset.asset_pk AND requests.approver = user_name.user_pk AND requests.source_fac = facility.facility_pk AND requests.request_pk = %s "
        Adata = the_id
        cur.execute(SQL, (Adata,))
        ac = cur.fetchone()
        #print ("what does a query return = ")
        #print (ac)

        rTime = str(ac[3])
        transit_txt = "" + ac[0] + " approved at " + rTime + " that " + ac[1] + " be moved from " + ac[2] + " to "
        
        SQL = "SELECT facility.facility_name FROM requests, facility WHERE requests.destination_fac = facility.facility_pk AND requests.request_pk = %s "
        Adata = the_id
        cur.execute(SQL, (Adata,))
        ac = cur.fetchone()
        #print ("what does a query return = ")
        #print (ac)
        
        transit_txt = transit_txt + "" + ac[0] + "."
        session['transit_text'] = transit_txt
        
        return render_template('update_transit.html')
    
    if request.method == 'POST':
        session['error'] = ""
        the_users = session['uname']
        the_id = session['id']
        
        #if request.form['facil'] and request.form['fcode'] and request.form['finfo']:
        if request.form['submit'] == 'Load':
            #the_times = datetime.datetime.strptime(request.form['load'], '%Y-%m-%dT%H:%M').isoformat()
            now = datetime.datetime.strptime(request.form['load'], '%Y-%m-%dT%H:%M')
            print(now)
            the_times = now.date().isoformat()
            print (the_times)

            SQL = "UPDATE transit SET load_time = %s WHERE transit_pk = %s;"
            Bdata = (the_times, the_id)
            cur.execute(SQL, Bdata)
            conn.commit()
            
            session['error'] = "Load time has been set."
            return render_template('dashboard.html')
        
        if request.form['submit'] == 'Unload':
            #the_times = datetime.datetime.strptime(request.form['unload'], '%Y-%m-%dT%H:%M').isoformat()
            now = datetime.datetime.strptime(request.form['unload'], '%Y-%m-%dT%H:%M')
            print(now)
            the_times = now.date().isoformat()
            print (the_times)

            #app_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M").isoformat()
            
            SQL = "UPDATE transit SET unload_time = %s WHERE transit_pk = %s;"
            Bdata = (the_times, the_id)
            cur.execute(SQL, Bdata)
            conn.commit()
            
            session['error'] = "Un-Load time has been set."
            return render_template('dashboard.html')
        
        session['error'] = "I don't know what button you pushed."
        return render_template('update_transit.html')
    
    session['error'] = "I don't know what you're trying to do."
    return render_template('update_transit.html')


## It seemed easier to have the html web page only use one route.
## So, this function figures out who is working and sends them to the appropriate page.
@app.route('/do_work', methods=['GET'])
def do_work():
    logisticsOfficer = "Logistics Officer"
    session['id'] = request.args['id']
    
    try:
        if session['role'] == logisticsOfficer:
            return render_template('update_transit.html')
        else:
            return render_template('approve_req.html')
    except:
        session['error'] = "You haven't logged in yet."
        return render_template('login.html')
    
    return render_template('dashboard.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    #session['works'] = ""
    logisticsOfficer = "Logistics Officer"
    try:
        if session['role'] == logisticsOfficer:
            SQL = "SELECT asset.asset_tag, transit.transit_pk FROM asset, transit WHERE asset.asset_pk = transit.asset_fk;"
        else:
            SQL = "SELECT asset.asset_tag, requests.request_pk FROM asset, requests WHERE asset.asset_pk = requests.asset_fk AND requests.approved = false AND requests.rejected = false;"
    except:
        session['error'] = "You haven't logged in yet."
        return render_template('login.html')
    
    cur.execute(SQL)
    fac = cur.fetchall()
    
    asset_name = []
    for f in fac:
        
        b = dict()
        b['asset_name']=f[0]
        #print ("add asset = ")
        #print (f[0])
        #print ("what is b = ")
        #print (b)
        
        b['id']=f[1]
        #print ("add id = ")
        #print (f[1])
        ##print ("what is b = ")
        #print (b)
        asset_name.append(b)
        
    session['works'] = asset_name

    print (session['works'])
        

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
            #the_times = datetime.datetime.strptime(request.form['time'], '%Y-%m-%dT%H:%M').isoformat()
            now = datetime.datetime.strptime(request.form['time'], '%Y-%m-%dT%H:%M')
            print(now)
            the_times = now.date().isoformat()
            print (the_times)


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
            #the_times = datetime.datetime.strptime(request.form['time'], '%Y-%m-%dT%H:%M').isoformat()
            now = datetime.datetime.strptime(request.form['time'], '%Y-%m-%dT%H:%M')
            print(now)
            the_times = now.date().isoformat()
            print (the_times)


            SQL = "SELECT asset_tag FROM asset WHERE asset_tag = %s;"
            Adata = the_asset
            cur.execute(SQL, (Adata,))
            db_row = cur.fetchone()
        
            if db_row is not None:

                SQL = "SELECT asset.asset_tag, asset_at.disposed FROM asset, asset_at WHERE asset.asset_pk=asset_at.asset_fk AND asset.asset_tag = %s AND asset_at.disposed = true;"
                Adata = the_asset
                cur.execute(SQL, (Adata,))
                db_row1 = cur.fetchone()
                print("delete?")
                print (db_row1)
                
                if db_row1 is None:
                    SQL = "SELECT asset.asset_pk, facility.facility_pk FROM asset, facility, asset_at WHERE asset.asset_tag = %s AND asset_at.asset_fk = asset.asset_pk AND asset_at.facility_fk = facility.facility_pk;"
                    Adata = the_asset
                    cur.execute(SQL, (Adata,))
                    db_ass = cur.fetchone()

                    the_info = list(db_ass)
                    the_info.append(the_times)
                    the_info2 = tuple(the_info)
                    
                    SQL = "UPDATE asset_at SET disposed = true FROM asset WHERE asset_at.asset_fk = asset.asset_pk AND asset.asset_tag = %s;"
                    Adata = the_asset
                    cur.execute(SQL, (Adata,))
                    conn.commit()
                    
                    SQL = "UPDATE asset_at SET depart = %s FROM asset WHERE asset_at.asset_fk = asset.asset_pk AND asset.asset_tag = %s;"
                    Bdata = (the_times, the_asset)
                    cur.execute(SQL, Bdata)
                    conn.commit()
                    
                    SQL = "INSERT INTO asset_at (asset_fk, facility_fk, depart, in_transit, disposed) VALUES (%s, %s, %s, false, true); "
                    #db_ass.append(the_times)
                    cur.execute(SQL, the_info2)
                    conn.commit()

                    session['Derror'] = "" + the_asset + " has been disposed of."
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
