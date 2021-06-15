#!/bin/bash
cd ~
git clone --depth 3 --filter=blob:none --sparse https://github.com/Lernni/E2-Anwesenheitserfassung-fuer-Modellflugplatz
cd ~/E2-Anwesenheitserfassung-fuer-Modellflugplatz/
git sparse-checkout set src/webserver/frontend/dist
cd src/webserver/frontend/dist
sudo rm -rf /var/www/vue/*.*
cp -r * /var/www/vue

cd ~/E2-Anwesenheitserfassung-fuer-Modellflugplatz/
git sparse-checkout set src/webserver/backend
cd src/webserver/backend
cp -r * ~/backend

cd ~/backend
source .venv/bin/activate
pip install -r requirements.txt
deactivate

sudo rm -rf ~/E2-Anwesenheitserfassung-fuer-Modellflugplatz/
sudo systemctl restart apache2
sudo killall python
sudo ~/backend/.venv/bin/python -m flask run &