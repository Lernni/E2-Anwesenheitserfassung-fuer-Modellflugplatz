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
pip install flask flask_restx
```
4. Flask App ausführen:
```
python3 -m flask run
```

Das Backend kann über http://localhost:5000/ erreicht werden und öffnet dort Swagger UI mit einer Übersicht über alle URLs der REST API.

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

### Einstellungen für VSCode
Für VSCode als Entwicklungsumgebung, lohnt sich die [Vetur Extension](https://marketplace.visualstudio.com/items?itemName=octref.vetur). Es ist aber empfehlenswert folgende Zeilen in die `settings.json` von VSCode anzufügen, um die veraltete Fehlermeldung `no-multiple-template-root` zu entfernen:

```
"vetur.validation.template": false,
"vetur.validation.script": false,
"vetur.validation.style": false,
```


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
? Please pick a preset: Manually select features
? Check the features needed for your project: Choose Vue version, Babel, Router, Linter
? Choose a version of Vue.js that you want to start the project with 3.x (Preview)
? Use history mode for router? (Requires proper server setup for index fallback in production) Yes
? Pick a linter / formatter config: Basic
? Pick additional lint features: Lint on save
? Where do you prefer placing config for Babel, ESLint, etc.? In package.json
? Save this as a preset for future projects? No
```

4. Abhängigkeiten installieren:

```
npm install axios
```