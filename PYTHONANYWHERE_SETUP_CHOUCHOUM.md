# Déploiement PythonAnywhere pour chouchoum

Ce guide explique comment déployer ton site Django sur PythonAnywhere avec le compte `chouchoum`.

## 1. Mettre à jour le dépôt GitHub

Le dépôt a déjà été mis à jour avec la correction WSGI nécessaire.

## 2. Déployer depuis PythonAnywhere Bash

Ouvre une console Bash sur PythonAnywhere et exécute :

```bash
cd ~
if [ -d ~/sdi_site ]; then
  cd ~/sdi_site && git pull origin master
else
  git clone https://github.com/cenadyonlineschool100-ui/sdi-marche-mondial-unit-50.git sdi_site
  cd ~/sdi_site
fi

cd ~/sdi_site/sdi_market
mkvirtualenv --python=/usr/bin/python3.12 sdi_venv 2>/dev/null || true
workon sdi_venv
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py check
```

## 3. Configurer la Web app PythonAnywhere

Dans l'onglet `Web` :

- Working directory : `/home/chouchoum/sdi_site/sdi_market`
- WSGI file : `sdi_market/sdi_market/wsgi.py`
- Virtualenv : `/home/chouchoum/.virtualenvs/sdi_venv`
- Python version : `3.12`

## 4. Variables d'environnement à ajouter

- `DJANGO_SETTINGS_MODULE = sdi_market.settings`
- `DEBUG = False`
- `ALLOWED_HOSTS = chouchoum.pythonanywhere.com`

## 5. Recharger

Clique sur `Reload chouchoum.pythonanywhere.com`.

## 6. Tester

Ouvre : `https://chouchoum.pythonanywhere.com/`

Si tu vois ton site Django et non la page Hello World, ton hébergement est actif.

## 7. En cas de problème

Envoie moi :

- le message exact du navigateur
- le contenu du `Error log`
- le contenu du `Server log`
