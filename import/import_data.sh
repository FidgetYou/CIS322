# Checks for correct amount of input
# Pretyy sure I got it from the teacher.
if [ "$#" -ne 2 ]; then
    echo "Usage: ./import_data.sh <dataBaseName> <folder>"
    exit;
fi

dropdb $1
pg_ctl -D $2 -l logfile start
createdb $1

python3 ./porter.py $1 5432 $2
