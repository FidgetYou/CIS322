There are 3 files in this folder.  This is one of them, right now.

The other two are python script files.

One of them adds users to the data base, the other rekoves their access to the database/website.

From the job's description: 

##
activate_user.py
##

Three arguments will be passed to activate_user.py. 
The first argument will be the host part of the URL for your LOST instance 
and will include a trailing '/' (e.g. http://127.0.0.1:8080/). 
The second argument will be the username to create or reactivate. 
The third argument will be the password to set for the user. 
The fourth argument will be the role for the user facofc or logofc 
for the facilities officer and logistics officer roles respectively.

python3 activate_user.py http://127.0.0.1:8080/ smith14 password facofc
(That's the important bit there at the end.)


##
revoke_user.py
##

Two arguments will be passed to revoke_user.py. 
The first argument will be the host part of the URL for your LOST instance 
and will include a trailing '/' (e.g. http://127.0.0.1:8080/). 
The second argument will be the username to revoke.

python3 revoke_user.py http://127.0.0.1:8080/ smith14

Enjoy!
