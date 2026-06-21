#!/bin/bash
# One-line deployment script for PythonAnywhere
# Copy and paste this entire script into PythonAnywhere bash console

set -e  # Exit on any error

echo "🚀 Starting PythonAnywhere deployment..."

# Step 1: Clone repo
echo "📥 Step 1: Cloning GitHub repository..."
cd ~ && git clone https://github.com/cenadyonlineschool100-ui/sdi-marche-mondial-unit-50.git sdi_site 2>/dev/null || (cd sdi_site && git pull origin master)

# Step 2: Create virtualenv
echo "🐍 Step 2: Creating virtualenv..."
mkvirtualenv --python=/usr/bin/python3.10 sdi_venv 2>/dev/null || workon sdi_venv

# Step 3: Navigate and install
echo "📦 Step 3: Installing dependencies..."
cd ~/sdi_site/sdi_market
workon sdi_venv
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1

# Step 4: Database migrations
echo "🔄 Step 4: Running migrations..."
python manage.py migrate --noinput

# Step 5: Collect static files
echo "📁 Step 5: Collecting static files..."
python manage.py collectstatic --noinput > /dev/null 2>&1

# Step 6: Generate config
echo "🔑 Step 6: Generating configuration..."
python generate_pythonanywhere_config.py > /home/$(whoami)/PYTHONANYWHERE_CONFIG.txt 2>&1 || true

echo ""
echo "✅ ✅ ✅ DEPLOYMENT COMPLETE! ✅ ✅ ✅"
echo ""
echo "📝 Next steps:"
echo "   1. Go to https://www.pythonanywhere.com/web_app_setup/"
echo "   2. Add new web app with:"
echo "      - Source code: /home/$(whoami)/sdi_site"
echo "      - Working dir: /home/$(whoami)/sdi_site/sdi_market"
echo "      - WSGI file: sdi_market/sdi_market/wsgi.py"
echo "   3. Add environment variables (see below)"
echo "   4. Click RELOAD"
echo "   5. Visit: https://$(whoami).pythonanywhere.com"
echo ""
echo "🔑 Environment variables to add:"
echo "   DJANGO_SETTINGS_MODULE=sdi_market.settings"
echo "   DEBUG=False"
echo "   ALLOWED_HOSTS=$(whoami).pythonanywhere.com"
echo ""
echo "For SECRET_KEY, see: /home/$(whoami)/PYTHONANYWHERE_CONFIG.txt"
echo ""
