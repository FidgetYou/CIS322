# Here lies a great many dead things. 
# Though I do not count myself as included here, 
# the love of the art and the time to appreciate it are.
# P.S. I'm bored.  ...And not in a good way.
# Comment, Like, and Subscribe if you agree! :-P

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

    
SQL = "SELECT user_name.username, user_name.password, role.role, user_name.active FROM asset, role WHERE asset.role_fk = role.role_pk "
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

        
SQL = "SELECT asset.asset_tag, facility.facility_code, facility_name FROM facility "
cur.execute(SQL)
ac = cur.fetchall()

with open(export_files[3], 'w') as out:
    writer = csv.writer(out)
    for f in ac:
        writer.writerow(f)
out.close()        


cur.close()
conn.close()
