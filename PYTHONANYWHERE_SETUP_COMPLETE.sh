#!/bin/bash
# Script prêt à coller dans une console Bash PythonAnywhere
# Remplacez YOUR_USERNAME par votre nom d'utilisateur PythonAnywhere
# Exécutez ce script ligne par ligne ou en bloc dans la console Bash PythonAnywhere

set -e

PA_USER=YOUR_USERNAME
PA_APPDIR=~/sdi_site
REPO_URL="https://github.com/cenadyonlineschool100-ui/sdi-marche-mondial-unit-50.git"
BRANCH=master
VENV_NAME=sdi_venv

echo "📥 Clonage / mise à jour du dépôt"
if [ -d "$PA_APPDIR" ]; then
    echo "Le répertoire existe, mise à jour..."
    cd "$PA_APPDIR"
    git fetch origin
    git checkout $BRANCH || true
    git pull origin $BRANCH
else
    echo "Clonage du dépôt dans $PA_APPDIR..."
    cd ~
    git clone "$REPO_URL" sdi_site
    cd "$PA_APPDIR"
fi

# Aller dans le répertoire Django
cd "$PA_APPDIR/sdi_market"

echo "🐍 Création / activation du virtualenv"
# Si mkvirtualenv n'est pas disponible, remplacez par python3 -m venv ~/.virtualenvs/$VENV_NAME
if command -v mkvirtualenv >/dev/null 2>&1; then
    mkvirtualenv --python=/usr/bin/python3.10 "$VENV_NAME" 2>/dev/null || true
    workon "$VENV_NAME"
else
    echo "mkvirtualenv introuvable — création d'un venv standard"
    python3 -m venv ~/.virtualenvs/$VENV_NAME
    source ~/.virtualenvs/$VENV_NAME/bin/activate
fi

echo "📦 Installation des dépendances"
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Optionnel: créer un .env minimal local (vous pouvez l'éditer après)
if [ ! -f .env ]; then
  echo "Création d'un fichier .env minimal"
  cat > .env <<EOF
DJANGO_SETTINGS_MODULE=sdi_market.settings
DEBUG=False
ALLOWED_HOSTS=${PA_USER}.pythonanywhere.com
DJANGO_SECRET_KEY=$(python - <<PY
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
PY
)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DATABASE_URL=sqlite:///db.sqlite3
EOF
fi

echo "🔄 Exécution des migrations"
python manage.py migrate --noinput

echo "📁 Collecte des fichiers statiques"
python manage.py collectstatic --noinput

echo "✅ Script terminé. Suivez ces instructions dans l'interface PythonAnywhere Web:"
echo "  - Working directory: /home/$PA_USER/sdi_site/sdi_market"
echo "  - WSGI file: sdi_market/sdi_market/wsgi.py"
echo "  - Virtualenv path (Web tab): /home/$PA_USER/.virtualenvs/$VENV_NAME"
echo "  - Env vars à ajouter:"
echo "      DJANGO_SETTINGS_MODULE=sdi_market.settings"
echo "      DEBUG=False"
echo "      ALLOWED_HOSTS=$PA_USER.pythonanywhere.com"

echo "Puis cliquez sur 'Reload' et ouvrez https://$PA_USER.pythonanywhere.com"

echo "Si vous rencontrez une erreur, copiez-collez le contenu du 'Error log' et 'Server log' ici pour que je vous aide."
