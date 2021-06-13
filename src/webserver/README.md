# Webserver

## Backend (Python Flask)
>Dokumentation Flask: https://flask.palletsprojects.com/en/1.1.x/<br>
Dokumentation Flask_RestX: https://flask-restx.readthedocs.io/en/latest/

### Installation

1. siehe https://code.visualstudio.com/docs/python/tutorial-flask
>Schritt 5: Python-Pfad: ./env/bin/python3<br>
Schritt 8 & 9: jeweils mit `python3` ausführen

2. Abhängigkeiten installieren:
```
pip install -r requirements.txt
```
4. Flask App ausführen:
```
python -m flask run
```

Das Backend kann über http://localhost:5000/ erreicht werden und öffnet dort Swagger UI mit einer Übersicht über alle URLs der REST API.

### Setup Datenbank für das Backend

```
cd backend
python make_server_db.py
```

## Frontend (Vue CLI v3)
>Dokumentation Vue CLI: https://cli.vuejs.org/guide/

### Lokale Einrichtung
Lokale Einrichtung des Repositories, wenn das Projekt bereits auf GitHub existiert.
>Hinweis: Der Ordner `node_modules` wird nicht mit gepusht, sondern lokal erzeugt. Die konkreten Abhängigkeiten für die lokale Einrichtung sind in der Datei `package.json` hinterlegt.

1. Node.js und npm installieren: https://www.npmjs.com/get-npm
2. `git pull`
3. Abhängigkeiten installieren:
```
cd frontend
npm install
```
4. Development-Server lokal starten:
```
npm run serve
```

Der Development-Server kann über http://localhost:8080/ erreicht werden.


### Installation (Ubuntu)
Nur, falls noch kein Projekt global erstellt wurde.

1. Node.js installieren:
```
sudo apt-get install -y nodejs
```
2. Vue CLI installieren:
```
sudo npm install -g @vue/cli
```
3. Neues Vue-Projekt anlegen und folgende Auswahl treffen:
```
vue create frontend
```

```
Vue CLI v4.5.12
? Please pick a preset: Manually select features
? Check the features needed for your project: Choose Vue version, Babel, Router, Linter
? Choose a version of Vue.js that you want to start the project with 2.x
? Use history mode for router? (Requires proper server setup for index fallback in production) Yes
? Pick a linter / formatter config: Basic
? Pick additional lint features: Lint on save
? Where do you prefer placing config for Babel, ESLint, etc.? In package.json
? Save this as a preset for future projects? No
```

## Deployment

### Einrichtung des Apache-Webservers
1. Installieren von Apache
```
sudo apt install apache2
```
2. Apache konfigurieren:
```
sudo mkdir /var/www/vue
sudo chown -R $USER:$USER /var/www/vue
sudo chmod -R 755 /var/www/vue

sudo a2enmod proxy
sudo a2ensite vue.conf
sudo a2dissite 000-default.conf
```

vue.conf erstellen
```
sudo nano /etc/apache2/sites-available/vue.conf
```
->
```
<VirtualHost *:80>
  ServerAdmin webmaster@localhost
  ServerName your_domain
  ServerAlias www.your_domain
  ProxyPreserveHost On
  ProxyPass /api http://localhost:5000/api
  ProxyPassReverse /api http://localhost:5000/api
  DocumentRoot /var/www/vue
  ErrorLog ${APACHE_LOG_DIR}/error.log
  CustomLog ${APACHE_LOG_DIR}/access.log combined

  <Directory "/var/www/vue">
    <IfModule mod_rewrite.c>
      RewriteEngine On
      RewriteBase /
      RewriteRule ^index\.html$ - [L]
      RewriteCond %{REQUEST_FILENAME} !-f
      RewriteCond %{REQUEST_FILENAME} !-d
      RewriteRule . /index.html [L]
    </IfModule>
  </Directory>
</VirtualHost>
```


### Frontend überführen
1. Build Frontend
```
npm run build
```

2. `/var/www/vue/` Ordnerinhalt löschen

3. `dist` Ordnerinhalt via scp nach `/var/www/vue/` kopieren

### Backend überführen
1. Python installieren
```
sudo apt install python
sudo apt install python3-pip
sudo pip3 install virtualenv
```

2. Backend Ordner erstellen
```
cd ~
sudo mkdir backend
sudo chown -R $USER:$USER ~/backend
sudo chmod -R 755 ~/backend
cd backend
```

3. Backend Ordnerinhalt via scp nach `~/backend/` kopieren
4. Python Abhängigkeiten vorbereiten und via scp nach `~/backend/` kopieren
```
pip freeze > requirements.txt
```

5. Python Venv erstellen
```
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

6. DB erstellen
```
python make_server_db.py
```

7. Backend starten
```
sudo ~/backend/.venv/bin/python -m flask run &
```