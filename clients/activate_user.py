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
    
    #print (sys.argv[0])
    #print (sys.argv[1])
    #print (sys.argv[2])
    #print (sys.argv[3])
    #print (sys.argv[4])
    
    the_addy = sys.argv[1]
    the_addy = "http://127.0.0.1:8080/"
    the_user = sys.argv[2]
    the_pass = sys.argv[3]
    the_role = sys.argv[4]
    
    # Setup the data to send
    #sargs = dict()
    """
    url = the_addy
    query = {'field': value}
    res = requests.post(url, data=query)
    print(res.text)
    
    """

    info = dict()
    info['name'] = the_user
    info['pass'] = the_pass
    info['role'] = the_role
    
    post_info = dict()
    post_info['arguments']=json.dumps(info)
    post_info['signature']=''
    data = urlencode(post_info)
    print("Sending:")
    print(data)
    route = the_addy
    
    the_request = Request(route,data.encode('ascii'),method='POST')
    
    the_responce = urlopen(the_request)
    the_reply = json.loads(the_responce.read().decode('ascii'))
    print(the_reply['error'])

    
