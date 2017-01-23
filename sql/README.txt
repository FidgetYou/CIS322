### create_tables.sql ###
	- This file uses SQL to create the database.

### import_data.sh ###
	- This file downloads the legacy data and uncompresses it.
	- Then this file runs a simple python script "snapped.py" with the instructions for where and what data needs to 
be inserted into the database.

### snapped.py ###
	- This file opens the CSV file it is told to
	- Reads the CSV file into a list
	- Inserts the requested fields from the CSV file into the database.

