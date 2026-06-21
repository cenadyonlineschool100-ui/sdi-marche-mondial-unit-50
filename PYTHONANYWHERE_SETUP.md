# ============================================
# Instructions pour PythonAnywhere
# ============================================

## ÉTAPE 1 : Se connecter à PythonAnywhere
Allez sur https://www.pythonanywhere.com et connectez-vous.

## ÉTAPE 2 : Ouvrir la console Bash
- Cliquez sur "Consoles" en haut
- Cliquez sur "Bash"
- Collez les commandes ci-dessous une par une

## ÉTAPE 3 : Exécuter les commandes dans la console

### Commande 1 : Cloner le dépôt GitHub
```bash
cd ~
git clone https://github.com/cenadyonlineschool100-ui/sdi-marche-mondial-unit-50.git sdi_site
cd ~/sdi_site/sdi_market
```

### Commande 2 : Créer un virtualenv
```bash
mkvirtualenv --python=/usr/bin/python3.10 sdi_venv
workon sdi_venv
```

### Commande 3 : Installer les dépendances
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Commande 4 : Exécuter les migrations
```bash
python manage.py migrate --noinput
```

### Commande 5 : Collecter les fichiers statiques
```bash
python manage.py collectstatic --noinput
```

## ÉTAPE 4 : Configurer l'application Web dans PythonAnywhere

1. Allez sur l'onglet "Web"
2. Cliquez sur "Add a new web app"
3. Choisissez "Python 3.10"
4. Remplissez les champs :
   - **Working directory** : /home/YOUR_USERNAME/sdi_site/sdi_market
   - **WSGI file** : sdi_market/sdi_market/wsgi.py

## ÉTAPE 5 : Ajouter les variables d'environnement

1. Dans l'onglet "Web", cherchez "Environment variables"
2. Cliquez sur "Add"
3. Ajoutez les variables :
   - Clé: `DJANGO_SETTINGS_MODULE` → Valeur: `sdi_market.settings`
   - Clé: `DEBUG` → Valeur: `False`
   - Clé: `ALLOWED_HOSTS` → Valeur: `YOUR_USERNAME.pythonanywhere.com`
   - Clé: `DJANGO_SECRET_KEY` → Valeur: `<une clé secrète>`

## ÉTAPE 6 : Recharger le site

1. Dans l'onglet "Web", cliquez sur le bouton "Reload YOUR_USERNAME.pythonanywhere.com"
2. Attendez 30 secondes
3. Ouvrez votre navigateur et allez à : https://YOUR_USERNAME.pythonanywhere.com

## ÉTAPE 7 : Vérifier si ça marche

- Si vous voyez votre site → ✅ Succès!
- Si vous voyez une erreur → vérifiez le "Error log" et "Server log" dans PythonAnywhere

## En cas d'erreur

1. Cliquez sur l'onglet "Web"
2. Descendez jusqu'à "Log files"
3. Ouvrez "Error log" et "Server log"
4. Cherchez les messages d'erreur
5. Les erreurs communes sont :
   - `ImportError` : Package mal installé
   - `ModuleNotFoundError` : `DJANGO_SETTINGS_MODULE` mal défini
   - `OperationalError` : Base de données non migrée
   - `ALLOWED_HOSTS` : Domaine non accepté

## Note importante

⚠️ PythonAnywhere n'est pas ideal pour les applications avec WebSockets/Channels.
Si vous voyez des erreurs liées à `channels`, `daphne`, ou `websocket`, c'est normal.
Le reste du site devrait fonctionner en HTTP classique.

## Besoin d'aide ?

Si quelque chose ne marche pas, envoyez-moi :
1. L'URL de votre site PythonAnywhere
2. Le contenu du "Error log" de PythonAnywhere
3. Le contenu du "Server log" de PythonAnywhere
