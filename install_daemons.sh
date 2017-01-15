echo "Starting Postgres Download"
git clone https://github.com/postgres/postgres.git
cd postgres
git checkout REL9_5_STABLE

echo "Configuring Postgres"
./configure --prefix=$HOME/$1/installed

echo "Make Postgres"
make
make install

cd ..
echo "Starting Apache Download"
curl http://supergsego.com/apache//httpd/httpd-2.4.25.tar.gz > httpd-2.4.25.tar.gz

tar -xzf httpd-2.4.25.tar.gz 

cd httpd-2.4.25

echo "Configuring Apache"
./configure --prefix=$HOME/$1/installed
make
make install

cd ..

