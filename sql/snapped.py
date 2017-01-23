# Here lies a great many dead things. 
# Though I do not count myself as included here, 
# the love of the art and the time to appreciate it are.
# P.S. I'm bored.  ...And not in a good way.
# Comment, Like, and Subscribe if you agree! :-P

import psycopg2
import sys
import csv
import datetime

arg3 = "./osnap_legacy/" + sys.argv[3]

with open(arg3, 'r') as f:
    reader = csv.reader(f)
    csv_list = list(reader)

#print (csv_list)

# Setup the database connection #
conn = psycopg2.connect(dbname=sys.argv[1],host='127.0.0.1',port=int(sys.argv[2]))
cur = conn.cursor()

for i in range (4, len(sys.argv), 3):
    #print ("i = " + str(i))
    for j in range (1, len(csv_list)):
        numb = int(sys.argv[i+2])
        #print ("insert into table %s on the row %s this value %s ", (sys.argv[i], sys.argv[i+1], csv_list[j][numb], ))    

        try:
            cur.execute("INSERT INTO %s ( %s ) VALUES ( %s ) ", ( sys.argv[i],  sys.argv[i+1], csv_list[j][numb], ))
        except Exception:
            print (csv[0][numb] + " had no information at entry #" + str(j))
 
conn.commit()

curr.close()
conn.close()
