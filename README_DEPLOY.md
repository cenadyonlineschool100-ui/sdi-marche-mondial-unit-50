# Déploiement GitHub + PythonAnywhere

## Ce qui a été fait

- Le dépôt local a été committé et poussé vers GitHub (`origin master`).
- Un script helper a été ajouté : `deploy_github_and_pythonanywhere.ps1`.
- Les fichiers de déploiement PythonAnywhere existent déjà : `deploy_pythonanywhere.sh` et `auto_deploy_pythonanywhere.py`.

## Étape 1 : Exécuter le helper local

Dans PowerShell, depuis le dossier du projet :

```powershell
Set-Location 'c:\wamp64\www\SDI STORE 1'
.\deploy_github_and_pythonanywhere.ps1
```

Ce script :

- vérifie les changements locaux
- commit et push sur GitHub
- affiche les commandes à copier dans PythonAnywhere Bash

## Étape 2 : Déployer sur PythonAnywhere

1. Connectez-vous sur https://www.pythonanywhere.com
2. Ouvrez une console Bash
3. Copiez-collez les commandes affichées par le script PowerShell

> Remplacez `YOUR_USERNAME` par votre nom d’utilisateur PythonAnywhere si nécessaire.

## Étape 3 : Configurer la Web App PythonAnywhere

Dans l’onglet `Web` de PythonAnywhere :

- Working directory : `/home/YOUR_USERNAME/sdi_site/sdi_market`
- WSGI file : `sdi_market/sdi_market/wsgi.py`
- Variables d’environnement :
  - `DJANGO_SETTINGS_MODULE=sdi_market.settings`
  - `DEBUG=False`
  - `ALLOWED_HOSTS=YOUR_USERNAME.pythonanywhere.com`

## Étape 4 : Recharger et vérifier

1. Cliquez sur `Reload` dans l’interface PythonAnywhere
2. Ouvrez : `https://YOUR_USERNAME.pythonanywhere.com`

## Limite

Je ne peux pas terminer le déploiement PythonAnywhere sans accéder à votre compte PythonAnywhere. Tout le reste est prêt et prêt à être collé/exécuté côté PythonAnywhere.
