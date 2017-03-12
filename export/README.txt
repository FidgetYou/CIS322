README.txt There is always one. 

export_data.sh - Here we have a bash/command line script that should check for and remove a given directory.
    Then recreate the directory so that it can be filled with some files and run the accompanying python file.
    usage should be something like:  
    
    bash export_data.sh <dbname> <output dir>  (minus the <> )
    

ex-porter.py - This is the python file. It should take the info from the previously mentioned database
    (The one you told export_data.sh about) and put it into four different CSV files.
    
    
    
(Sorry if there are any typos. The FireFox spellchecker isn't working in Git's editor window.)
