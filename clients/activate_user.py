import sys
import json
import datetime
import argparse

from urllib.request import Request, urlopen
from urllib.parse   import urlencode

# Three arguments will be passed to activate_user.py. 
# The first argument will be the host part of the URL for your LOST instance and will include a trailing '/' 
# (e.g. http://127.0.0.1:8080/). 
# The second argument will be the username to create or reactivate. 
# The third argument will be the password to set for the user. 
# The fourth argument will be the role for the user facofc or logofc 
# for the facilities officer and logistics officer roles respectively. 

# python3 activate_user.py http://127.0.0.1:8080/ smith14 password facofc

if __name__ == '__main__':
    
    print (sys.argv[0])
    print (sys.argv[1])
    print (sys.argv[2])
    print (sys.argv[3])
    print (sys.argv[4])
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('route', type=str)
    parser.add_argument('name', type=str)
    parser.add_argument('password', type=str)
    parser.add_argument('role', type=str)
    args = parser.parse_args()
    route = args.route

    arg_dict = dict()
    arg_dict['name'] = args.name
    arg_dict['role'] = args.role
    arg_dict['password'] = args.password


    # Print a message to let the user know what is being tried
    print("Activating user: %s"%arg_dict['name'])

    # Setup the data to send
    sargs = dict()
    sargs['arguments']=json.dumps(arg_dict)
    sargs['signature']=''
    data = urlencode(sargs)
    print("sending:\n%s"%data)
    
    # Make the resquest
    req = Request(route,data.encode('ascii'),method='POST')
    print('requst made')
    
    res = urlopen(req)
    # Parse the response
    resp = json.loads(res.read().decode('ascii'))
print("Call to LOST returned: %s"%resp['result'])
"""
    
