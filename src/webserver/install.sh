#!/bin/bash
apt install -y apache2 python python3-pip curl
pip3 install virtualenv

mkdir /var/www/vue
chown -R $USER:$USER /var/www/vue
chmod -R 755 /var/www/vue

curl "https://github.com/Lernni/E2-Anwesenheitserfassung-fuer-Modellflugplatz/tree/master/src/webserver/vue.conf" > /etc/apache2/sites-available/vue.conf

a2enmod proxy proxy_http rewrite
a2ensite vue.conf
a2dissite 000-default.conf

curl "https://github.com/Lernni/E2-Anwesenheitserfassung-fuer-Modellflugplatz/tree/master/src/webserver/frontend/dist/" > /var/www/vue/

mkdir ~/backend
chown -R $USER:$USER ~/backend
chmod -R 755 ~/backend

cd ~/backend
virtualenv .venv

curl "https://github.com/Lernni/E2-Anwesenheitserfassung-fuer-Modellflugplatz/tree/master/src/webserver/backend/" > ~/backend/

source .venv/bin/activate
pip install -r requirements.txt
python make_server_db.py
deactivate

systemctl restart apache2
~/backend/.venv/bin/python -m flask run &