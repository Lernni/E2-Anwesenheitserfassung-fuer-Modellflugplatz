#!/bin/bash
dir="/home/ubuntu"

sudo add-apt-repository ppa:git-core/ppa
sudo apt update
sudo apt install -y apache2 python python3-pip git
sudo pip3 install virtualenv

cd $dir
git clone --depth 3 --filter=blob:none --sparse https://github.com/Lernni/E2-Anwesenheitserfassung-fuer-Modellflugplatz
cd $dir/E2-Anwesenheitserfassung-fuer-Modellflugplatz/
git sparse-checkout set src/webserver/vue.conf
cd src/webserver
sudo cp ./vue.conf /etc/apache2/sites-available/

sudo a2enmod proxy proxy_http rewrite
sudo a2ensite vue.conf
sudo a2dissite 000-default.conf

sudo mkdir /var/www/vue
sudo chown -R $USER:$USER /var/www/vue
sudo chmod -R 755 /var/www/vue

cd $dir/E2-Anwesenheitserfassung-fuer-Modellflugplatz/
git sparse-checkout set src/webserver/frontend/dist
cd src/webserver/frontend/dist
sudo rm -rf /var/www/vue/*.*
cp -r -v * /var/www/vue

sudo mkdir $dir/backend
sudo chown -R $USER:$USER $dir/backend
sudo chmod -R 755 $dir/backend

cd $dir/E2-Anwesenheitserfassung-fuer-Modellflugplatz/
git sparse-checkout set src/webserver/backend
cd src/webserver/backend
cp -r -v *.* $dir/backend

cd $dir/backend
sudo virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
python make_server_db.py
deactivate

sudo rm -rf $dir/E2-Anwesenheitserfassung-fuer-Modellflugplatz/
sudo systemctl restart apache2
sudo killall python
sudo $dir/backend/.venv/bin/python -m flask run &