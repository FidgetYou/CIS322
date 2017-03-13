import psycopg2
import sys
import csv
import datetime
from os.path import expanduser
#home = expanduser("~")

import_files = [ '/users.csv', '/facilities.csv', '/assets.csv', '/transfers.csv' ]
#arg3 = "./osnap_legacy/" + sys.argv[3]
#arg1 = "" + home + sys.argv[1]
users_head = ( 'username', 'password', 'role', 'active')
facilities_head = ( 'fcode', 'common_name' )
assets_head = ( 'asset_tag', 'description', 'facility', 'acquired', 'disposed' )
transfers_head = ( 'asset_tag', 'request_by', 'request_dt', 'approve_by', 'approve_dt', 'source', 'destination', 'load_dt', 'unload_dt' )



#print (csv_list)

# Setup the database connection #
try:
    conn = psycopg2.connect(dbname=sys.argv[1],host='127.0.0.1',port=int(sys.argv[2]))
    cur = conn.cursor()
except:
    sys.exit("Unable to connect to the database.")

#for f in import_files:
if import_files:
    arg3 = "" + sys.argv[3] + import_files[0]

    try:
        with open(arg3, 'r') as f:
            reader = csv.reader(f)
            csv_list = list(reader)
    except:
        sys.exit("Unable to find the file " + arg3)    
    
    
    for i in range (1, len(csv_list)):
        #print ("i = " + str(i))
        #for j in range (1, len(csv_list)):
            #numb = int(sys.argv[i+2])
            #thing1 = sys.argv[i]
            #thing1 = thing1.replace("`", "")
            #thing1 = thing1.replace("'", "")

            #thing2 = sys.argv[i+1]
            #thing3 = csv_list[j][numb]

        #print ("insert into table %s on the row %s this value %s ", (sys.argv[i].replace("'", ""), sys.argv[i+1], csv_list[j][numb], ))    
        #for j in csv_list[i]
        the_username = "" + csv_list[i][0] + ""
        the_password = "" + csv_list[i][1] + ""
        active = "" + csv_list[i][3] + ""
        if csv_list[i][2] == 'Logistics Officer':
            role_fk = '1'
        else:
            print("not Logistics Officer?")
            role_fk = '2'
                
            
        SQL = "INSERT INTO user_name (username, password, role_fk, active) VALUES (%s, %s, %s, %s);"
        data = (the_username, the_password, role_fk, active)
        cur.execute(SQL, data)
        conn.commit()
        
        #thing1 = 'user_name'
        #curQuery = "INSERT INTO "+thing1+" ("+thing2+") VALUES ('"+thing3+"');"

        #try:
        #    cur.execute(curQuery)
        #    #print ( "Inserted "+thing3+" into table "+thing1)
        #except Exception:
        #    print (csv_list[0][numb] + " had no information at entry #" + str(j))
    f.close()
        
        
        
        
    arg3 = "" + sys.argv[3] + import_files[1]

    try:
        with open(arg3, 'r') as f:
            reader = csv.reader(f)
            csv_list = list(reader)
    except:
        sys.exit("Unable to find the file " + arg3)    
    f.close()
    
    for i in range (1, len(csv_list)):
        the_code = "" + csv_list[i][0] + ""
        the_name = "" + csv_list[i][1] + ""       
            
        SQL = "INSERT INTO facility (facility_name, facility_code) VALUES (%s, %s);"
        data = (the_name, the_code)
        cur.execute(SQL, data)
        conn.commit()
        
        
        
        
    arg3 = "" + sys.argv[3] + import_files[2]
    try:
        with open(arg3, 'r') as f:
            reader = csv.reader(f)
            csv_list = list(reader)
    except:
        sys.exit("Unable to find the file " + arg3)    
    f.close()
    
    for i in range (1, len(csv_list)):
        the_tag = "" + csv_list[i][0] + ""
        the_des = "" + csv_list[i][1] + ""     
        the_fac = "" + csv_list[i][2] + "" 
        arrive = "" + csv_list[i][3] + "" 
        if csv_list[i][4]:
            #depart = csv_list[i][4]
            depart = None
        else:
            #depart = "" + csv_list[i][4] + "" 
            depart = None
            
            
        SQL = "INSERT INTO asset (asset_tag, asset_info) VALUES (%s, %s);"
        data = (the_tag, the_des)
        cur.execute(SQL, data)
        conn.commit()
        
        SQL = """INSERT INTO asset_at (asset_fk, facility_fk, arrive, depart) VALUES 
        ( (SELECT asset_pk from asset WHERE asset_tag = %s),
        (SELECT facility_pk from facility WHERE facility_name = %s),
        %s, %s );"""
        data = (the_tag, the_fac, arrive, depart)
        cur.execute(SQL, data)
        conn.commit()
        
        if depart == "null":
            SQL = "UPDATE asset_at SET disposed = true FROM asset WHERE asset_at.asset_fk = asset.asset_pk AND asset.asset_tag = %s;"
            Adata = the_tag
            cur.execute(SQL, (Adata,))
            conn.commit()
    
    
    
    
    
    
    
    arg3 = "" + sys.argv[3] + import_files[3]
    try:
        with open(arg3, 'r') as f:
            reader = csv.reader(f)
            csv_list = list(reader)
    except:
        sys.exit("Unable to find the file " + arg3)    
    f.close()
    
    for i in range (1, len(csv_list)):
        asset_tag = "" + csv_list[i][0] + ""
        request_by = "" + csv_list[i][1] + ""     
        request_dt = "" + csv_list[i][2] + "" 
        approve_by = "" + csv_list[i][3] + "" 
        approve_dt = "" + csv_list[i][4] + "" 
        source = "" + csv_list[i][5] + ""
        destination = "" + csv_list[i][6] + ""     
        load_dt = "" + csv_list[i][7] + "" 
        unload_dt = "" + csv_list[i][8] + "" 
        
        if load_dt == "":
            load_dt = null
        if unload_dt == "":
            unload_dt = null
        if approve_by == "":
            approve_by = null
        if approve_dt == "":
            approve_dt = null
            
        SQL = """INSERT INTO requests (asset_fk, requester, approver, source_fac, destination_fac, request_time, approve_time ) 
        VALUES 
        ( (SELECT asset_pk from asset WHERE asset_tag = %s),
        (SELECT user_pk from user_name WHERE user_pk = %s),
        (SELECT user_pk from user_name WHERE user_pk = %s),
        (SELECT facility_pk from facility WHERE facility_name = %s),
        (SELECT facility_pk from facility WHERE facility_name = %s),
        %s, %s );"""
        data = (asset_tag, request_by, approve_by, source, destination, request_dt, approve_dt)
        cur.execute(SQL, data)
        conn.commit()
        
        SQL = """INSERT INTO transit (asset_fk, source_fac, destination_fac, load_time, unload_time) VALUES 
        ( (SELECT asset_pk from asset WHERE asset_tag = %s),
        (SELECT facility_pk from facility WHERE facility_code = %s),
        (SELECT facility_pk from facility WHERE facility_code = %s),
        %s, %s );"""
        data = (asset_tag, source, destination, load_dt, unload_dt)
        cur.execute(SQL, data)
        conn.commit()




conn.commit()

cur.close()
conn.close()
