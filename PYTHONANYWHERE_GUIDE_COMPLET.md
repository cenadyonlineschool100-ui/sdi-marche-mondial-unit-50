# 🚀 Guide Complet : Hébergement sur PythonAnywhere

## 📋 Plan

```
Étape 1: Cloner le dépôt GitHub          [5 min]
    ↓
Étape 2: Créer un virtualenv             [3 min]
    ↓
Étape 3: Installer les dépendances       [10 min]
    ↓
Étape 4: Exécuter les migrations         [5 min]
    ↓
Étape 5: Collecter les fichiers statiques [5 min]
    ↓
Étape 6: Configurer le WSGI              [5 min]
    ↓
Étape 7: Ajouter les variables d'env     [5 min]
    ↓
Étape 8: Tester le site                  [5 min]

Total estimé : ~45 minutes
```

---

## 📍 Étape 1 : Cloner le dépôt GitHub

**Où**: Console Bash de PythonAnywhere
**Commande** :

```bash
cd ~
git clone https://github.com/cenadyonlineschool100-ui/sdi-marche-mondial-unit-50.git sdi_site
cd ~/sdi_site/sdi_market
```

✅ Vérifier : `ls -la` doit montrer les dossiers `marketplace/`, `beauty/`, etc.

---

## 🐍 Étape 2 : Créer un virtualenv

**Où**: Console Bash
**Commande** :

```bash
mkvirtualenv --python=/usr/bin/python3.12 sdi_venv
workon sdi_venv
```

✅ Vérifier : le prompt doit afficher `(sdi_venv) user@server`

---

## 📦 Étape 3 : Installer les dépendances

**Où**: Console Bash (avec virtualenv actif)
**Commande** :

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

⚠️ Cela peut prendre 5-10 minutes. Attendez jusqu'à la fin.

✅ Vérifier : `pip list | grep Django` doit montrer Django 6.0.3

---

## 🔄 Étape 4 : Exécuter les migrations

**Où**: Console Bash (avec virtualenv actif)
**Commande** :

```bash
python manage.py migrate --noinput
```

✅ Vérifier : doit afficher `Running migrations: ... OK`

---

## 📁 Étape 5 : Collecter les fichiers statiques

**Où**: Console Bash (avec virtualenv actif)
**Commande** :

```bash
python manage.py collectstatic --noinput
```

✅ Vérifier : doit afficher `X static files copied to './staticfiles'`

---

## ⚙️ Étape 6 : Configurer le WSGI

**Où**: PythonAnywhere Web App Configuration
**Lien** : https://www.pythonanywhere.com/web_app_setup/

### 6.1 - Créer l'application Web
1. Cliquez sur `Add a new web app`
2. Choisissez `Python 3.10`
3. Continue

### 6.2 - Configurer les chemins

Dans l'onglet "Web":

| Champ | Valeur |
|-------|--------|
| **Source code** | `/home/YOUR_USERNAME/sdi_site` |
| **Working directory** | `/home/YOUR_USERNAME/sdi_site/sdi_market` |
| **WSGI configuration file** | `/home/YOUR_USERNAME/sdi_site/sdi_market/sdi_market/wsgi.py` |

✅ Remplacez `YOUR_USERNAME` par votre username réel (ex: `john123`)

---

## 🔑 Étape 7 : Ajouter les variables d'environnement

**Où**: PythonAnywhere Web App → Environment variables

### 7.1 - Ajouter chaque variable

Cliquez sur "Add" et remplissez :

#### Variable 1:
- Clé: `DJANGO_SETTINGS_MODULE`
- Valeur: `sdi_market.settings`

#### Variable 2:
- Clé: `DEBUG`
- Valeur: `False`

#### Variable 3:
- Clé: `ALLOWED_HOSTS`
- Valeur: `YOUR_USERNAME.pythonanywhere.com`

#### Variable 4:
- Clé: `DJANGO_SECRET_KEY`
- Valeur: `<copier une clé depuis generate_pythonanywhere_config.py>`

#### Variable 5 (optionnel - pour développement local):
- Clé: `EMAIL_BACKEND`
- Valeur: `django.core.mail.backends.console.EmailBackend`

---

## 🔄 Étape 8 : Recharger et tester

**Où**: PythonAnywhere Web App

### 8.1 - Recharger l'application
1. Cliquez sur le bouton **"Reload YOUR_USERNAME.pythonanywhere.com"**
2. Attendez 30-60 secondes

### 8.2 - Tester dans le navigateur
Ouvrez: `https://YOUR_USERNAME.pythonanywhere.com`

### 8.3 - Que voir?
- ✅ Votre site s'affiche normalement
- ❌ Erreur 500 ou 400 = vérifier les logs

---

## 🔍 Diagnostiquer les erreurs

**Où**: PythonAnywhere Web App → Log files

### Si erreur 500 ou 400:

1. Ouvrez **"Error log"**
2. Cherchez les erreurs comme :
   - `ModuleNotFoundError: No module named 'sdi_market'` → virtualenv mal configuré
   - `OperationalError: no such table` → migrations non exécutées
   - `ALLOWED_HOSTS` → domaine non reconnu
   - `ImportError` → dépendance manquante

3. Envoyez les logs pour que j'aide à corriger

---

## 📞 Checklist de vérification

- [ ] GitHub dépôt cloné dans `/home/YOUR_USERNAME/sdi_site`
- [ ] Virtualenv créé avec Python 3.10
- [ ] `pip install -r requirements.txt` ✅
- [ ] `python manage.py migrate` ✅
- [ ] `python manage.py collectstatic` ✅
- [ ] WSGI file pointé vers `sdi_market/wsgi.py`
- [ ] Variables d'env ajoutées (au moins DJANGO_SETTINGS_MODULE)
- [ ] Web app reloadée
- [ ] Site accessible via `https://YOUR_USERNAME.pythonanywhere.com`

---

## ✅ Succès!

Si vous voyez votre site, bravo 🎉!

Le site est maintenant hébergé sur PythonAnywhere et accessible 24/7.

---

## ⚠️ Points importants

1. **Fichiers de médias** : PythonAnywhere ne conserve pas les uploads entre redémarrages. Utilisez un service externe (S3, etc.) pour les médias.

2. **WebSockets** : `channels` et `daphne` ne fonctionnent pas bien sur PythonAnywhere. Certaines fonctionnalités temps réel peuvent échouer.

3. **Base de données** : SQLite est dans `/home/YOUR_USERNAME/sdi_site/sdi_market/db.sqlite3`. Pour la production, utilisez PostgreSQL.

4. **SSL** : Votre site a HTTPS par défaut avec PythonAnywhere.

---

## 🆘 Besoin d'aide ?

Si quelque chose ne marche pas :
1. Envoyez le contenu du **"Error log"**
2. Envoyez le contenu du **"Server log"**
3. Décrivez ce que vous voyez
4. Je diagnostiquerai et corrigerai

Bonne chance! 🚀
