#from flask import Flask, render_template, redirect, url_for, session, flash, request
import sys
import json
import datetime
import argparse
#import requests

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
    
    if len(sys.argv) < 5 :
        sys.exit("Usage: python3 %s <url> <username> <password> <role>" %sys.argv[0])
    
    
    the_addy = sys.argv[1] + "activate_user"
    the_user = sys.argv[2]
    the_pass = sys.argv[3]
    the_role = sys.argv[4]
    
    # Setup the data to send
    args = dict()
    args['name'] = the_user
    args['pass'] = the_pass
    args['role'] = the_role
    
    data = urlencode(args)
    print("Sending:")
    print(data)
    route = the_addy
    
    req = Request(route,data.encode('ascii'),method='POST')
    
    res = urlopen(req)

    result = str(res.read())[1:]
    
    print(result)

    
