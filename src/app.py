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
        SQL = "SELECT facility_name FROM facility"""
        cur.execute(SQL)
        res = cur.fetchall()
        facility_names = []
        for f in fac:
            a = dict()
            a['facility_name']=a[0]
            facility_names.append(a)
        session['facilities'] = facility_names
        
        
        return render_template('facility.html')

    if request.method == 'POST':
        session['error'] = ""
        if request.form['facil'] and request.form['fcode'] and request.form['finfo']:
            the_flity = "'" + request.form['facil'] + "'"
            the_fcode = "'" + request.form['fcode'] + "'"
            the_finfo = "'" + request.form['finfo'] + "'"
        
            SQL = "SELECT facility_name, facility_code FROM facility WHERE facility_name = %s AND facility_code = %s;"
            data = (the_flity,the_fcode)
            cur.execute(SQL, data)
            db_row = cur.fetchone()
        
            if db_row is None:
                SQL = "INSERT INTO facility (facility_name, facility_code, facility_info) VALUES (%s, %s, %s);"
                data = (the_flity, the_fcode, the_finfo)
                cur.execute(SQL, data)
                conn.commit()

            session['error'] = "Facility " + the_flity + " has been added to the database."
            return render_template('facility.html')
        
        else:
            session['error'] = "Please fill all of the boxes."
            return render_template('facility.html')



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
    """return render_template('welcome.html',dbname=dbname,dbhost=dbhost,dbport=dbport)"""

@app.route('/rest/list_products', methods=('POST',))
def list_products():
    """This function is huge... much of it should be broken out into other supporting
        functions"""
    
    # Check maybe process as plaintext
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])
    # Unmatched, take the user somewhere else
    else:
        redirect('rest')
    
    # Setup a connection to the database
    conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
    cur  = conn.cursor()
    
    # If execution gets here we have request json to work with
    # Do I need to handle compartments in this query?
    if len(req['compartments'])==0:
        print("have not compartment")
        # Just handle vendor and description
        SQLstart = """select vendor,description,string_agg(c.abbrv||':'||l.abbrv,',')
from products p
left join security_tags t on p.product_pk=t.product_fk
left join sec_compartments c on t.compartment_fk=c.compartment_pk
left join sec_levels l on t.level_fk=l.level_pk"""
        if req['vendor']=='' and req['description']=='':
            # No filters, add the group by and query is ready to go
            SQLstart += " group by vendor,description"
            cur.execute(SQLstart)
        else:
            if not req['vendor']=='' and not req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                req['description']="%"+req['description']+"%"
                SQLstart += " where description ilike %s and vendor ilike %s group by vendor,description"
                cur.execute(SQLstart,(req['description'],req['vendor']))
            elif req['vendor']=='':
                req['description']="%"+req['description']+"%"
                SQLstart += " where description ilike %s group by vendor,description"
                cur.execute(SQLstart,(req['description'],))
            elif req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                SQLstart += " where vendor ilike %s group by vendor,description"
                cur.execute(SQLstart,(req['vendor'],))
    else:
        print("have compartment %s"%len(req['compartments']))
        # Need to handle compartments too
        SQLstart = """select vendor,description,string_agg(c.abbrv||':'||l.abbrv,',')
from security_tags t
left join sec_compartments c on t.compartment_fk=c.compartment_pk
left join sec_levels l on t.level_fk=l.level_pk
left join products p on t.product_fk=p.product_pk
where product_fk is not NULL and c.abbrv||':'||l.abbrv = ANY(%s)"""
        if req['vendor']=='' and req['description']=='':
            # No filters, add the group by and query is ready to go
            SQLstart += " group by vendor,description,product_fk having count(*)=%s"
            cur.execute(SQLstart,(req['compartments'],len(req['compartments'])))
        else:
            if not req['vendor']=='' and not req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                req['description']="%"+req['description']+"%"
                SQLstart += " and description ilike %s and vendor ilike %s group by vendor,description,product_fk having count(*)=%s"
                cur.execute(SQLstart,(req['compartments'],req['description'],req['vendor'],len(req['compartments'])))
            elif req['vendor']=='':
                req['description']="%"+req['description']+"%"
                SQLstart += " and description ilike %s group by vendor,description,product_fk having count(*)=%s"
                cur.execute(SQLstart,(req['compartments'],req['description'],len(req['compartments'])))
            elif req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                SQLstart += " and vendor ilike %s group by vendor,description,product_fk having count(*)=%s"
                cur.execute(SQLstart,(req['compartments'],req['vendor'],len(req['compartments'])))
    
    # One of the 8 cases should've run... process the results
    dbres = cur.fetchall()
    listing = list()
    for row in dbres:
        e = dict()
        e['vendor'] = row[0]
        e['description'] = row[1]
        if row[2] is None:
            e['compartments'] = list()
        else:
            e['compartments'] = row[2].split(',')
        listing.append(e)
    
    # Prepare the response
    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['listing'] = listing
    data = json.dumps(dat)
    
    conn.close()
    return data
    
@app.route('/rest/suspend_user', methods=('POST',))
def suspend_user():
    # Try to handle as plaintext
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])

    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
