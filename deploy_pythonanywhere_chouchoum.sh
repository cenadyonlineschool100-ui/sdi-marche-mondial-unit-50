#!/bin/bash

# ============================================
# Déploiement PythonAnywhere pour le compte chouchoum
# ============================================

set -e

APP_DIR=~/sdi_site
VENV_NAME=sdi_venv
REPO_URL=https://github.com/cenadyonlineschool100-ui/sdi-marche-mondial-unit-50.git
PYTHONANYWHERE_HOST=chouchoum.pythonanywhere.com

# 1. Cloner ou mettre à jour le dépôt GitHub
cd ~
if [ -d "$APP_DIR" ]; then
  echo "📥 Mise à jour du dépôt existant..."
  cd "$APP_DIR"
  git pull origin master
else
  echo "📥 Clonage du dépôt GitHub..."
  git clone "$REPO_URL" "$(basename "$APP_DIR")"
  cd "$APP_DIR"
fi

# 2. Créer ou utiliser le virtualenv
if [ ! -d "$HOME/.virtualenvs/$VENV_NAME" ]; then
  echo "🐍 Création du virtualenv $VENV_NAME..."
  mkvirtualenv --python=/usr/bin/python3.12 "$VENV_NAME"
fi
source "$HOME/.virtualenvs/$VENV_NAME/bin/activate"

# 3. Installer les dépendances
cd "$APP_DIR/sdi_market"
echo "📦 Installation des dépendances..."
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt

# 4. Créer le fichier .env si nécessaire
if [ ! -f .env ]; then
  echo "⚙️ Création du fichier .env..."
  cat > .env << EOF
DJANGO_SETTINGS_MODULE=sdi_market.settings
DEBUG=False
ALLOWED_HOSTS=$PYTHONANYWHERE_HOST
DJANGO_SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EOF
fi

# 5. Exécuter les migrations et collectstatic
echo "🔄 Exécution des migrations..."
python manage.py migrate --noinput

echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "✅ Déploiement local PythonAnywhere terminé."

cat << EOF

Suivez ces étapes dans l'interface PythonAnywhere Web:
  1. Working directory: /home/chouchoum/sdi_site/sdi_market
  2. WSGI file: sdi_market/sdi_market/wsgi.py
  3. Virtualenv: /home/chouchoum/.virtualenvs/$VENV_NAME
  4. Add environment variables:
       DJANGO_SETTINGS_MODULE=sdi_market.settings
       DEBUG=False
       ALLOWED_HOSTS=$PYTHONANYWHERE_HOST
  5. Cliquez sur Reload
  6. Visitez: https://$PYTHONANYWHERE_HOST

EOF
