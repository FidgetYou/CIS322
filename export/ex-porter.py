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


arg3 = "./osnap_legacy/" + sys.argv[3]
arg1 = "" + home + sys.argv[1]

with open(arg3, 'r') as f:
    reader = csv.reader(f)
    csv_list = list(reader)

#print (csv_list)

# Setup the database connection #
try:
    conn = psycopg2.connect(dbname=sys.argv[1],host='127.0.0.1',port=int(sys.argv[2]))
except:
    print("Unable to connect to the database.")

cur = conn.cursor()

for i in range (4, len(sys.argv), 3):
    #print ("i = " + str(i))
    for j in range (1, len(csv_list)):
        numb = int(sys.argv[i+2])
        thing1 = sys.argv[i]
        thing1 = thing1.replace("`", "")
        thing1 = thing1.replace("'", "")

        thing2 = sys.argv[i+1]
        thing3 = csv_list[j][numb]

        #print ("insert into table %s on the row %s this value %s ", (sys.argv[i].replace("'", ""), sys.argv[i+1], csv_list[j][numb], ))    

        curQuery = "INSERT INTO "+thing1+" ("+thing2+") VALUES ('"+thing3+"');"

        try:
            cur.execute(curQuery)
            #print ( "Inserted "+thing3+" into table "+thing1)
        except Exception:
            print (csv_list[0][numb] + " had no information at entry #" + str(j))

 
conn.commit()

cur.close()
conn.close()
