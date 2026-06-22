#!/bin/bash
# Script de test à exécuter dans une console Bash PythonAnywhere pour chouchoum
# Il vérifie le virtualenv, Django, la configuration WSGI, et les logs.

set -e

PA_USER=chouchoum
VENV_DIR=~/.virtualenvs/sdi_venv
PROJECT_DIR=~/sdi_site/sdi_market
WSGI_FILE=/var/www/chouchoum_pythonanywhere_com_wsgi.py
ERROR_LOG=/var/log/chouchoum.pythonanywhere.com.error.log
SERVER_LOG=/var/log/chouchoum.pythonanywhere.com.server.log

printf "\n=== PythonAnywhere site readiness test for %s ===\n" "$PA_USER"

echo "1) Vérifier l'existence du projet"
if [ ! -d "$PROJECT_DIR" ]; then
  echo "ERREUR: projet introuvable: $PROJECT_DIR"
  exit 1
fi

cd "$PROJECT_DIR"

echo "2) Vérifier le virtualenv"
if [ ! -d "$VENV_DIR" ]; then
  echo "ERREUR: virtualenv introuvable: $VENV_DIR"
  exit 1
fi

source "$VENV_DIR/bin/activate"

echo "3) Vérifier la version de Python et Django"
python --version
python -c "import django; print('Django', django.get_version())"

echo "4) Vérifier le fichier WSGI"
if [ ! -f "$WSGI_FILE" ]; then
  echo "ERREUR: WSGI file introuvable: $WSGI_FILE"
  exit 1
fi

echo "Contenu du fichier WSGI (premières 20 lignes):"
head -n 20 "$WSGI_FILE"

echo "5) Vérifier les paramètres Django"
python - <<PY
from pathlib import Path
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdi_market.settings')
try:
    import django
    print('DJANGO_SETTINGS_MODULE is set and Django imports correctly')
except Exception as exc:
    print('ERREUR Django import:', exc)
    raise
PY

echo "6) Vérifier les logs d'erreur récents"
if [ -f "$ERROR_LOG" ]; then
  echo "--- Dernières lignes du error.log ---"
  tail -n 20 "$ERROR_LOG"
else
  echo "Aucun fichier error.log trouvé: $ERROR_LOG"
fi

if [ -f "$SERVER_LOG" ]; then
  echo "--- Dernières lignes du server.log ---"
  tail -n 20 "$SERVER_LOG"
else
  echo "Aucun fichier server.log trouvé: $SERVER_LOG"
fi

echo "\n=== Test terminé ==="
echo "Si toutes les étapes précédentes sont passées sans message ERREUR, le site est probablement prêt."
echo "Reste à vérifier dans l'onglet Web que le WSGI file, le virtualenv, et les variables d'environnement sont corrects, puis à cliquer sur Reload."
