#!/bin/bash
# Script à exécuter dans une console Bash PythonAnywhere pour chouchoum
# Cette version est compatible avec Python 3.12 / 3.13 et corrige WSGI et le virtualenv.

set -e

PA_USER=chouchoum
PA_APPDIR=~/sdi_site
REPO_URL="https://github.com/cenadyonlineschool100-ui/sdi-marche-mondial-unit-50.git"
VENV_DIR=~/.virtualenvs/sdi_venv
WSGI_FILE=/var/www/chouchoum_pythonanywhere_com_wsgi.py
PROJECT_DIR=/home/$PA_USER/sdi_site/sdi_market

echo "📥 Mise à jour du dépôt"
if [ -d "$PA_APPDIR" ]; then
  cd "$PA_APPDIR"
  git fetch origin
  git checkout master || true
  git pull origin master
else
  cd ~
  git clone "$REPO_URL" sdi_site
  cd "$PA_APPDIR"
fi

# Aller dans le projet Django
cd "$PROJECT_DIR"

# Choisir Python 3.13 ou 3.12
if command -v python3.13 >/dev/null 2>&1; then
  PYTHON=python3.13
elif command -v python3.12 >/dev/null 2>&1; then
  PYTHON=python3.12
else
  PYTHON=python3
fi

echo "🐍 Utilisation de $PYTHON pour créer/mettre à jour le virtualenv"
rm -rf "$VENV_DIR" || true
$PYTHON -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

echo "📦 Installation des dépendances"
pip install --upgrade pip setuptools wheel
pip install -r ../requirements.txt

echo "⚙️ Création du fichier .env minimal"
cat > .env <<'EOF'
DJANGO_SETTINGS_MODULE=sdi_market.settings
DEBUG=False
ALLOWED_HOSTS=chouchoum.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://chouchoum.pythonanywhere.com
DJANGO_SECRET_KEY=REPLACE_WITH_SECURE_SECRET
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DATABASE_URL=sqlite:///db.sqlite3
EOF

python - <<'PY'
from django.core.management.utils import get_random_secret_key
print('DJANGO_SECRET_KEY=' + get_random_secret_key())
PY

echo "🔄 Exécution des migrations"
python manage.py migrate --noinput

echo "📁 Collecte des fichiers statiques"
python manage.py collectstatic --noinput

echo "✅ Déploiement local terminé"

echo "Vérifie/colle ensuite ce contenu dans $WSGI_FILE si nécessaire :"
echo "---------------------------------------------"
echo "import os"
echo "import sys"
echo "from pathlib import Path"
echo "" 

echo "PROJECT_DIR = Path('/home/chouchoum/sdi_site/sdi_market')"
echo "sys.path.insert(0, str(PROJECT_DIR))"
echo "sys.path.insert(0, str(PROJECT_DIR / 'sdi_market'))"
echo "" 

echo "os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get('DJANGO_SETTINGS_MODULE', 'sdi_market.settings'))"
echo "" 

echo "from django.core.wsgi import get_wsgi_application"
echo "application = get_wsgi_application()"
echo "---------------------------------------------"

echo "Ensuite, configure la web app PythonAnywhere comme suit :"
echo "  Working directory: /home/chouchoum/sdi_site/sdi_market"
echo "  WSGI file: /var/www/chouchoum_pythonanywhere_com_wsgi.py"
echo "  Virtualenv: /home/chouchoum/.virtualenvs/sdi_venv"
echo "  Environment variables:"
echo "    DJANGO_SETTINGS_MODULE=sdi_market.settings"
echo "    DEBUG=False"
echo "    ALLOWED_HOSTS=chouchoum.pythonanywhere.com"
echo "    CSRF_TRUSTED_ORIGINS=https://chouchoum.pythonanywhere.com"
echo "Puis clique sur Reload et ouvre https://chouchoum.pythonanywhere.com"
