#!/bin/bash

# ============================================
# Script de déploiement PythonAnywhere
# À exécuter dans la console PythonAnywhere
# ============================================

echo "📦 Début du déploiement sur PythonAnywhere..."

# ============================================
# 1. Cloner ou mettre à jour le dépôt GitHub
# ============================================
echo "📥 Étape 1: Cloner le dépôt GitHub..."

if [ -d ~/sdi-marche-mondial-unit-50 ]; then
    echo "Le dépôt existe déjà, mise à jour..."
    cd ~/sdi-marche-mondial-unit-50
    git pull origin master
else
    echo "Clonage du dépôt..."
    cd ~
    git clone https://github.com/cenadyonlineschool100-ui/sdi-marche-mondial-unit-50.git
    cd ~/sdi-marche-mondial-unit-50
fi

# ============================================
# 2. Créer un virtualenv (si nécessaire)
# ============================================
echo "🐍 Étape 2: Configuration du virtualenv..."

if [ ! -d ~/venv ]; then
    echo "Création du virtualenv..."
    mkvirtualenv --python=/usr/bin/python3.10 venv
fi

workon venv

# ============================================
# 3. Installer les dépendances
# ============================================
echo "📦 Étape 3: Installation des dépendances..."

cd ~/sdi-marche-mondial-unit-50/sdi_market
pip install --upgrade pip
pip install -r requirements.txt

# ============================================
# 4. Configurer les variables d'environnement
# ============================================
echo "⚙️ Étape 4: Configuration des variables d'environnement..."

# Créer le fichier .env
cat > .env << EOF
DJANGO_SETTINGS_MODULE=sdi_market.settings
DEBUG=False
ALLOWED_HOSTS=YOUR_USERNAME.pythonanywhere.com
DJANGO_SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EOF

echo "✅ Fichier .env créé"

# ============================================
# 5. Exécuter les migrations
# ============================================
echo "🔄 Étape 5: Exécution des migrations..."

cd ~/sdi-marche-mondial-unit-50/sdi_market
python manage.py migrate --noinput

# ============================================
# 6. Collecter les fichiers statiques
# ============================================
echo "📁 Étape 6: Collecte des fichiers statiques..."

python manage.py collectstatic --noinput

# ============================================
# 7. Afficher les prochaines étapes
# ============================================
echo ""
echo "✅ DÉPLOIEMENT PRESQUE TERMINÉ!"
echo ""
echo "📝 Maintenant, dans PythonAnywhere Web App:"
echo "   1. Set 'Working directory' to: /home/YOUR_USERNAME/sdi-marche-mondial-unit-50/sdi_market"
echo "   2. Set 'WSGI file' to: sdi_market/sdi_market/wsgi.py"
echo "   3. Add environment variable: DJANGO_SETTINGS_MODULE=sdi_market.settings"
echo "   4. Click 'Reload YOUR_USERNAME.pythonanywhere.com'"
echo ""
echo "🌐 Accédez à: https://YOUR_USERNAME.pythonanywhere.com"
echo ""
