# 🚀 DÉPLOIEMENT RAPIDE SUR PYTHONANYWHERE

## 📌 TL;DR (30 secondes)

Copie cette commande **UNE SEULE FOIS** dans la console Bash de PythonAnywhere:

```bash
cd ~ && git clone https://github.com/cenadyonlineschool100-ui/sdi-marche-mondial-unit-50.git sdi_site && cd sdi_site/sdi_market && mkvirtualenv --python=/usr/bin/python3.10 sdi_venv && workon sdi_venv && pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

Puis configure dans l'interface web PythonAnywhere (5 minutes).

---

## ⚙️ CONFIGURATION PYTHONANYWHERE (après le script)

1. **Accès**: https://www.pythonanywhere.com

2. **Onglet Web** → **Add a new web app**

3. **Configuration**:
   - **Working directory**: `/home/YOUR_USERNAME/sdi_site/sdi_market`
   - **WSGI file**: `/home/YOUR_USERNAME/sdi_site/sdi_market/sdi_market/wsgi.py`

4. **Environment variables** (Add):
   - `DJANGO_SETTINGS_MODULE` = `sdi_market.settings`
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = `YOUR_USERNAME.pythonanywhere.com`
   - `DJANGO_SECRET_KEY` = (copier depuis la sortie du script)

5. **Reload** → bouton "Reload YOUR_USERNAME.pythonanywhere.com"

6. **Test**: https://YOUR_USERNAME.pythonanywhere.com

---

## 📍 REMPLACE "YOUR_USERNAME"

Où trouver ton username PythonAnywhere ?
- Regarde l'URL en haut à gauche : `https://www.pythonanywhere.com/user/YOUR_USERNAME/`
- Ou regarde ton domaine : `YOUR_USERNAME.pythonanywhere.com`

Exemple: Si tu t'appelles "john123", remplace `YOUR_USERNAME` par `john123`.

---

## ✅ CHECKLIST

- [ ] Bash console: Copie-colle la commande ci-dessus
- [ ] Attends 10-15 minutes que tout s'installe
- [ ] Vérifier: `ls -la ~/sdi_site/sdi_market/db.sqlite3` (doit exister)
- [ ] PythonAnywhere: Configure le WSGI file
- [ ] PythonAnywhere: Ajoute les variables d'env
- [ ] PythonAnywhere: Click RELOAD
- [ ] Attend 30 secondes
- [ ] Ouvre ton navigateur: `https://YOUR_USERNAME.pythonanywhere.com`
- [ ] Vois tu ton site? ✅ C'est bon!

---

## 🆘 EN CAS D'ERREUR

### Erreur 500 ou blanc

1. Va dans: https://www.pythonanywhere.com/web_app_setup/
2. Scroll down à "Log files"
3. Ouvre "Error log"
4. Envoie le contenu du log

### Erreurs communes

| Erreur | Solution |
|--------|----------|
| `ModuleNotFoundError` | Virtualenv mal configuré dans PythonAnywhere |
| `OperationalError: no such table` | Migrations non exécutées |
| `ALLOWED_HOSTS invalid` | Domaine mal configuré |
| `ImportError: No module named` | `pip install` a échoué |

---

## 📞 BESOIN D'AIDE?

Fournis:
1. Le contenu du "Error log" PythonAnywhere
2. Le contenu du "Server log" PythonAnywhere
3. Ton username PythonAnywhere

---

## 🎉 SUCCÈS!

Si ton site s'affiche → Bravo! C'est live! 🚀

Ton site est maintenant hébergé sur PythonAnywhere et accessible 24/7.
