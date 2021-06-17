#!/bin/bash
dir="/home/ubuntu"

cd $dir
git clone --depth 3 --filter=blob:none --sparse https://github.com/Lernni/E2-Anwesenheitserfassung-fuer-Modellflugplatz
cd $dir/E2-Anwesenheitserfassung-fuer-Modellflugplatz/
git sparse-checkout set src/webserver/frontend/dist
cd src/webserver/frontend/dist
sudo rm -rf /var/www/vue/*.*
cp -r -v * /var/www/vue

cd $dir/E2-Anwesenheitserfassung-fuer-Modellflugplatz/
git sparse-checkout set src/webserver/backend
cd src/webserver/backend
cp -r -v * $dir/backend

cd $dir/backend
source .venv/bin/activate
pip install -r requirements.txt
deactivate

sudo rm -rf $dir/E2-Anwesenheitserfassung-fuer-Modellflugplatz/
sudo systemctl restart apache2
sudo killall python
sudo $dir/backend/.venv/bin/python -m flask run &