#!/bin/bash
sudo add-apt-repository ppa:git-core/ppa
sudo apt update
sudo apt install -y apache2 python python3-pip git
sudo pip3 install virtualenv

cd ~
git clone --depth 3 --filter=blob:none --sparse https://github.com/Lernni/E2-Anwesenheitserfassung-fuer-Modellflugplatz
cd ~/E2-Anwesenheitserfassung-fuer-Modellflugplatz/
git sparse-checkout set src/webserver/vue.conf
cd src/webserver
sudo cp ./vue.conf /etc/apache2/sites-available/

sudo a2enmod proxy proxy_http rewrite
sudo a2ensite vue.conf
sudo a2dissite 000-default.conf

sudo mkdir /var/www/vue
sudo chown -R $USER:$USER /var/www/vue
sudo chmod -R 755 /var/www/vue

cd ~/E2-Anwesenheitserfassung-fuer-Modellflugplatz/
git sparse-checkout set src/webserver/frontend/dist
cd src/webserver/frontend/dist
sudo rm -rf /var/www/vue/*.*
cp -r * /var/www/vue

sudo mkdir ~/backend
sudo chown -R $USER:$USER ~/backend
sudo chmod -R 755 ~/backend

cd ~/E2-Anwesenheitserfassung-fuer-Modellflugplatz/
git sparse-checkout set src/webserver/backend
cd src/webserver/backend
cp -r * ~/backend

cd ~/backend
sudo virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
python make_server_db.py
deactivate

sudo rm -rf ~/E2-Anwesenheitserfassung-fuer-Modellflugplatz/
sudo systemctl restart apache2
sudo killall python
sudo ~/backend/.venv/bin/python -m flask run &