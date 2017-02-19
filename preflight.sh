echo "This file was copy/typed from the lost repo."

# BASH if statements! Cool!
# Checks for correct amount of input

if [ "$#" -ne 1 ]; then
    echo "Usage: ./preflight.sh <dataBaseName>"
    exit;
fi

# Create the SQL tables and maybe import/input some data

cd sql
psql $1 -f create_tables.sql
#curl -O https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz
#tar -xzf osnap_legacy.tar.gz
#bash ./import_data.sh $1 5432
#rm -rf osnap_legacy osnap_legacy.tar.gz
cd ..


# This is for installing/maving files to wsgi

cp -R src/* $HOME/wsgi



