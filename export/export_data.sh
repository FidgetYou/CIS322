# Checks for correct amount of input
# Pretyy sure I got it from the teacher.
if [ "$#" -ne 2 ]; then
    echo "Usage: ./preflight.sh <dataBaseName> <folder>"
    exit;
fi


# I found this on Stack Overflow

if [ -d "$2" ]; then 
  if [ -L "$2" ]; then
    # It is a symlink!
    # Symbolic link specific commands go here.
    rm -r "$2"
  else
    # It's a directory!
    # Directory command goes here.
    rm -r "$2"
  fi
fi
ourpath="$(pwd)"

mkdir $2
cd $2
touch users.csv
touch facilities.csv
touch assets.csv
touch transfers.csv

cd
echo $ourpath
cd $ourpath
ls
python3 ./ex-porter.py $1 5432 $2
