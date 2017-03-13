# My ex-porter exported X ports.

import psycopg2
import sys
import csv
import datetime
from os.path import expanduser
home = expanduser("~")

export_files = [ 'users.csv', 'facilities.csv', 'assets.csv', 'transfers.csv' ]
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
    for f in ac:
        writer.writerow(f)
out.close()  

        
SQL = "SELECT asset.asset_tag, asset.asset_info, facility.facility_code, asset_at.arrive, asset_at.depart FROM asset, facility, asset_at WHERE asset.asset_pk = asset_at.asset_fk AND asset_at.facility_fk = facility.facility_pk "
cur.execute(SQL)
ac = cur.fetchall()

with open(export_files[2], 'w') as out:
    writer = csv.writer(out)
    for f in ac:
        writer.writerow(f)
out.close()  

        
#SQL = "SELECT asset.asset_pk, asset.asset_tag, user_name.username, requests.request_time, facility.facility_code FROM asset, facility, requests, user_name WHERE asset.asset_pk = requests.asset_fk AND user_name.user_pk = requests.requester AND facility.facility_pk = source_fac ORDER BY asset.asset_pk "
#cur.execute(SQL)
#ac = cur.fetchall()

#SQL = "SELECT asset.asset_pk, user_name.username, requests.approve_time, facility.facility_code, transit.load_time, transit.unload_time FROM asset, facility, user_name, requests, transit WHERE asset.asset_pk = requests.asset_fk AND user_name.user_pk = requests.approver AND facility.facility_pk = requests.destination_fac ORDER BY asset.asset_pk "
#SQL = "SELECT asset.asset_pk, user_name.username, requests.approve_time, facility.facility_code, transit.load_time, transit.unload_time FROM asset, facility, user_name, requests, transit WHERE asset.asset_pk = requests.asset_fk AND user_name.user_pk = requests.approver AND facility.facility_pk = requests.destination_fac ORDER BY asset.asset_pk "
#cur.execute(SQL)
#dc = cur.fetchall()

#SQL = "SELECT requests.request_pk, asset.asset_tag, user_name.username, requests.request_time, facility.facility_code FROM asset, facility, requests, user_name WHERE requests.asset_fk = asset.asset_pk AND requests.requester = user_name.user_pk AND requests.source_fac = facility.facility_pk ORDER BY asset.asset_pk;"
#cur.execute(SQL)
#ac = cur.fetchall()
SQL = """SELECT asset.asset_tag, u.username, r.request_time, uu.username, r.approve_time, f.facility_code, ff.facility_code, transit.load_time, transit.unload_time
FROM requests r
LEFT JOIN asset a ON r.asset_fk = a.asset_pk
LEFT JOIN user_name u ON r.requester = u.user_pk
LEFT JOIN user_name uu ON r.approver = uu.user_pk
LEFT JOIN facility f ON r.source_fac = f.user_pk
LEFT JOIN facility ff ON r.destination_fac = ff.user_pk
LEFT JOIN transit t ON t.asset_fk = a.asset_pk"""
cur.execute(SQL)
ac = cur.fetchall()

# ac=Alternating Current, dc= Direct Current, fc= Fluctuating Current...?
print ("ac")
print (ac)
#print ("dc")
#print (dc)
if ac:
    with open(export_files[3], 'w') as out:
        writer = csv.writer(out)
        #for i in xrange(len(ac)):
        for i in ac:
            #fc.append([ac[i][1], ac[i][2], ac[i][3], dc[i][1], dc[i][2], ac[i][4], dc[i][3], dc[i][4], dc[i][5]])
            writer.writerow(ac)
    out.close()
    
else:
    sys.exit("I may have selected the DB incorrectly.")


cur.close()
conn.close()
