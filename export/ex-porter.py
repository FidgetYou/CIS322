# My ex-porter exported X ports.

import psycopg2
import sys
import csv
import datetime
from os.path import expanduser
home = expanduser("~")

export_files = [ 'users.csv', 'facilities.csv', 'assets.csv', 'transfers.csv' ]
users_head = ( 'username', 'password', 'role', 'active')
facilities_head = ( 'fcode', 'common_name' )
assets_head = ( 'asset_tag', 'description', 'facility', 'acquired', 'disposed' )
transfers_head = ( 'asset_tag', 'request_by', 'request_dt', 'approve_by', 'approve_dt', 'source', 'destination', 'load_dt', 'unload_dt' )

#arg3 = "$HOME/" + sys.argv[3]
#arg1 = "" + home + sys.argv[1]

#with open(arg3, 'r') as f:
#    reader = csv.reader(f)
#    csv_list = list(reader)

#print (csv_list)

# Setup the database connection #
try:
    conn = psycopg2.connect(dbname=sys.argv[1],host='127.0.0.1',port=int(sys.argv[2]))
    cur = conn.cursor()
except:
    sys.exit("Unable to connect to the database.")

    
SQL = "SELECT user_name.username, user_name.password, role.role, user_name.active FROM user_name, role WHERE user_name.role_fk = role.role_pk "
cur.execute(SQL)
ac = cur.fetchall()
#print ("what does a query return = ")
#print (ac)
       
#asset_trsf = []
#for f in ac:

with open(export_files[0], 'w') as out:
    writer = csv.writer(out)
    writer.writerow(users_head)
    for f in ac:
        writer.writerow(f)
out.close()          
#b = dict()
#b['asset_name']=f[0]
#b['facility_name']=f[1]
#asset_trsf.append(b)

#session['assets_transfer'] = asset_trsf

SQL = "SELECT facility_code, facility_name FROM facility "
cur.execute(SQL)
ac = cur.fetchall()

with open(export_files[1], 'w') as out:
    writer = csv.writer(out)
    writer.writerow(facilities_head)
    for f in ac:
        writer.writerow(f)
out.close()  

        
SQL = """SELECT asset.asset_tag, asset.asset_info, facility.facility_code, asset_at.arrive, asset_at.depart 
FROM asset
LEFT JOIN asset_at ON asset_at.asset_fk = asset.asset_pk
LEFT JOIN facility ON asset_at.facility_fk = facility_pk
"""
#WHERE asset.asset_pk = asset_at.asset_fk AND asset_at.facility_fk = facility.facility_pk;"""
cur.execute(SQL)
ac = cur.fetchall()

with open(export_files[2], 'w') as out:
    writer = csv.writer(out)
    writer.writerow(assets_head)
    for f in ac:
        writer.writerow(f)
out.close()  

SQL = """SELECT a.asset_tag, u.username, r.request_time, uu.username, r.approve_time, f.facility_code, ff.facility_code, t.load_time, t.unload_time
FROM requests r
LEFT JOIN asset a ON r.asset_fk = a.asset_pk
LEFT JOIN user_name u ON r.requester = u.user_pk
LEFT JOIN user_name uu ON r.approver = uu.user_pk
LEFT JOIN facility f ON r.source_fac = f.facility_pk
LEFT JOIN facility ff ON r.destination_fac = ff.facility_pk
LEFT JOIN transit t ON t.asset_fk = a.asset_pk"""
cur.execute(SQL)
ac = cur.fetchall()

# ac=Alternating Current, dc= Direct Current, fc= Fluctuating Current...?
#print ("ac")
#print (ac)

if ac:
    with open(export_files[3], 'w') as out:
        writer = csv.writer(out)
        writer.writerow(transfers_head)
        for i in ac:
            writer.writerow(ac)
    out.close()
    
else:
    sys.exit("I may have selected the DB incorrectly.")


cur.close()
conn.close()
