# Checks for correct amount of input
# Pretyy sure I got it from the teacher.
if [ "$#" -ne 2 ]; then
    echo "Usage: ./import_data.sh <dataBaseName> <folder>"
    exit;
fi
ourpath="$(pwd)"
dropdb $1
pg_ctl -D /home/osnapdev/import -l logfile start
createdb $1

cd ..
bash ./preflight.sh $1
cd import

python3 ./porter.py $1 5432 $2
