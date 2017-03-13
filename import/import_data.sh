# Checks for correct amount of input
# Pretyy sure I got it from the teacher.
if [ "$#" -ne 2 ]; then
    echo "Usage: ./import_data.sh <dataBaseName> <folder>"
    exit;
fi

python3 ./porter.py $1 5432 $2
