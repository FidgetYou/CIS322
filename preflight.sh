echo "This file was copy/typed from the lost repo, but copies to flask directory."

if [ "$#" -ne 1 ]; then
    echo "Usage: ./preflight.sh <dataBaseName>"
    exit;
fi

cd sql
psql $1 -f create_tables.sql
curl -O https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz
tar -xzf osnap_legacy.tar.gz
bash ./import_data.sh $1 5432
rm -rf osnap_legacy osnap_legacy.tar.gz
cd ..

# This says it is for installing wsgi files
# but I think I was going to go with the flask option
# so I don't know if they actually need to be copied.
# oh well, fingers crossed.

cp -R src/* $HOME/wsgi



