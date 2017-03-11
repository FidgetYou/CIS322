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

mkdir $2
cd $2
touch users.csv
touch facilities.csv
touch assets.csv
touch transfers.csv

python3 ex-porter.py $1 5432 $2
