<#
.SYNOPSIS
  Commit and push local changes to GitHub, then display PythonAnywhere deployment commands.
.DESCRIPTION
  This script stages all local changes, commits them if needed, pushes to the master branch,
  and prints the commands to run on PythonAnywhere to clone/update the repo, install dependencies,
  run migrations, collect static files, and configure the web app.
#>

param(
    [string]$CommitMessage = "Déploiement vers GitHub et préparation PythonAnywhere",
    [string]$GithubBranch = "master",
    [string]$RepoUrl = "https://github.com/cenadyonlineschool100-ui/sdi-marche-mondial-unit-50.git",
    [string]$PythonAnywhereAppDir = "sdi_site",
    [string]$VirtualEnvName = "sdi_venv"
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 Début du déploiement GitHub..." -ForegroundColor Cyan
Write-Host "`n📝 Vérification du dépôt Git..." -ForegroundColor Yellow

# Récupère l'état du dépôt
$status = (git status --porcelain) -join "`n"
if (-not [string]::IsNullOrWhiteSpace($status)) {
    Write-Host "`n📦 Changements détectés, staging et commit..." -ForegroundColor Yellow
    git add -A
    git commit -m "$CommitMessage"
} else {
    Write-Host "✅ Aucun changement à committer." -ForegroundColor Green
}

Write-Host "`n☁️  Push vers GitHub ($GithubBranch)..." -ForegroundColor Yellow
git push origin $GithubBranch

Write-Host "`n✅ Push GitHub réussi !" -ForegroundColor Green

Write-Host "`n📌 Maintenant, copiez-collez ces commandes dans une console Bash PythonAnywhere :" -ForegroundColor Cyan

$paCommands = @"
==============================================================
cd ~
if [ -d ~/$PythonAnywhereAppDir ]; then
  cd ~/$PythonAnywhereAppDir && git pull origin $GithubBranch
else
  git clone $RepoUrl $PythonAnywhereAppDir
  cd ~/$PythonAnywhereAppDir
fi
cd ~/$PythonAnywhereAppDir/sdi_market
mkvirtualenv --python=/usr/bin/python3.12 $VirtualEnvName 2>/dev/null || true
workon $VirtualEnvName
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py collectstatic --noinput
==============================================================
Ensuite, configurez l'application Web PythonAnywhere :
  - Working directory : /home/YOUR_USERNAME/$PythonAnywhereAppDir/sdi_market
  - WSGI file       : sdi_market/sdi_market/wsgi.py
  - Variables d'environnement :
      DJANGO_SETTINGS_MODULE=sdi_market.settings
      DEBUG=False
      ALLOWED_HOSTS=YOUR_USERNAME.pythonanywhere.com
==============================================================
Visitez ensuite : https://YOUR_USERNAME.pythonanywhere.com
"@

Write-Host $paCommands
