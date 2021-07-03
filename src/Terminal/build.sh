#!/bin/bash
dir="/home/pi"

cd $dir
mkdir Terminal
cd Terminal
sudo rm -rf *
git clone --depth 3 --filter=blob:none --sparse https://github.com/Lernni/E2-Anwesenheitserfassung-fuer-Modellflugplatz
cd $dir/Terminal/E2-Anwesenheitserfassung-fuer-Modellflugplatz/
git sparse-checkout set src/Terminal
cd src/Terminal

cp -r -v * $dir/Terminal

pip3 install -r requirements.txt

sudo rm -rf $dir/Terminal/E2-Anwesenheitserfassung-fuer-Modellflugplatz/
