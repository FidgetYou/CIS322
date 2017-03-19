import sys
import json
import datetime
import argparse

from urllib.request import Request, urlopen
from urllib.parse   import urlencode

# Two arguments will be passed to revoke_user.py. 
# The first argument will be the host part of the URL for your LOST instance 
# and will include a trailing '/' (e.g. http://127.0.0.1:8080/). 
#The second argument will be the username to revoke.

# python3 revoke_user.py http://127.0.0.1:8080/ smith14

if __name__ == '__main__':
    
    #print (sys.argv[0])
    #print (sys.argv[1])
    #print (sys.argv[2])
    #print (sys.argv[3])
    #print (sys.argv[4])
    if len(sys.argv) < 3 :
        sys.exit("Usage: python3 %s <url> <username>" %sys.argv[0])
    
    
    the_addy = sys.argv[1] + "revoke_user"
    the_user = sys.argv[2]
    
    args = dict()
    args['name'] = the_user
    
    
    data = urlencode(args)
    print("Sending:")
    print(data)
    route = the_addy
    
    req = Request(route,data.encode('ascii'),method='POST')
    
    res = urlopen(req)
    
    result = str(res.read())[1:]
    
    print(result)
