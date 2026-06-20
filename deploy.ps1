# Script d'automatisation: Git Push + Fly.io Deploy
# Usage: .\deploy.ps1 "message de commit"

param(
    [Parameter(Mandatory=$true)]
    [string]$commitMessage = "Mise à jour automatique",
    
    [switch]$skipFlyDeploy = $false
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 Début du déploiement..." -ForegroundColor Cyan

# 1. Vérifier l'état du repo
Write-Host "`n📝 Vérification du repo Git..." -ForegroundColor Yellow
git status

# 2. Stage tous les changements
Write-Host "`n📦 Staging des changements..." -ForegroundColor Yellow
git add -A

# 3. Vérifier s'il y a des changements
$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "✅ Aucun changement à committer" -ForegroundColor Green
    exit 0
}

# 4. Commit
Write-Host "`n💾 Commit: $commitMessage" -ForegroundColor Yellow
git commit -m $commitMessage

# 5. Push vers GitHub
Write-Host "`n☁️  Push vers GitHub..." -ForegroundColor Yellow
git push origin main 2>&1 | Tee-Object -Variable pushOutput
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors du push GitHub" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Push réussi vers GitHub!" -ForegroundColor Green

# 6. Deploy sur Fly.io (optionnel)
if (-not $skipFlyDeploy) {
    Write-Host "`n🚀 Déploiement sur Fly.io..." -ForegroundColor Yellow
    
    # Vérifier si flyctl est installé
    $flyCmd = Get-Command flyctl -ErrorAction SilentlyContinue
    if ($flyCmd) {
        flyctl deploy --remote-only
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Déploiement Fly.io réussi!" -ForegroundColor Green
        } else {
            Write-Host "⚠️  Erreur Fly.io (GitHub Actions prendra la relève si configuré)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "⚠️  flyctl non installé. GitHub Actions gère le déploiement." -ForegroundColor Yellow
    }
}

Write-Host "`n✨ Déploiement terminé!" -ForegroundColor Green
