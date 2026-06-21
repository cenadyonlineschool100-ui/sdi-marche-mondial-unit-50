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
 git status --short

$status = git status --porcelain
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
Write-Host "=============================================================="
Write-Host "cd ~"
Write-Host "if [ -d \~/$PythonAnywhereAppDir ]; then"
Write-Host "  cd \~/$PythonAnywhereAppDir && git pull origin $GithubBranch"
Write-Host "else"
Write-Host "  git clone $RepoUrl $PythonAnywhereAppDir"
Write-Host "  cd \~/$PythonAnywhereAppDir"
Write-Host "fi"
Write-Host "cd \~/$PythonAnywhereAppDir/sdi_market"
Write-Host "mkvirtualenv --python=/usr/bin/python3.10 $VirtualEnvName 2>/dev/null || true"
Write-Host "workon $VirtualEnvName"
Write-Host "pip install --upgrade pip setuptools wheel"
Write-Host "pip install -r requirements.txt"
Write-Host "python manage.py migrate --noinput"
Write-Host "python manage.py collectstatic --noinput"
Write-Host "=============================================================="
Write-Host "Ensuite, configurez l'application Web PythonAnywhere :" -ForegroundColor Cyan
Write-Host "  - Working directory : /home/YOUR_USERNAME/$PythonAnywhereAppDir/sdi_market"
Write-Host "  - WSGI file       : sdi_market/sdi_market/wsgi.py"
Write-Host "  - Variables d'environnement :"
Write-Host "      DJANGO_SETTINGS_MODULE=sdi_market.settings"
Write-Host "      DEBUG=False"
Write-Host "      ALLOWED_HOSTS=YOUR_USERNAME.pythonanywhere.com"
Write-Host "=============================================================="
Write-Host "Visitez ensuite : https://YOUR_USERNAME.pythonanywhere.com" -ForegroundColor Green
