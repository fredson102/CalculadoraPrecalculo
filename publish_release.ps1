<#
publish_release.ps1
Automatiza los pasos para publicar un release y disparar la workflow en GitHub.
Requisitos:
 - Git instalado y configurado
 - (Recomendado) GitHub CLI (`gh`) instalado y autenticado con `gh auth login`

Uso:
  PowerShell:
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    .\publish_release.ps1 -RepoUrl "https://github.com/tu-usuario/tu-repo.git" -Version v1.0.0

Si `-RepoUrl` no se proporciona y `gh` está instalado, el script usará `gh repo create` para crear el repo y empujar.
#>

param(
    [string]$RepoUrl = "",
    [string]$Version = "v1.0.0",
    [switch]$Force
)

function Check-Command($cmd) {
    $null -ne (Get-Command $cmd -ErrorAction SilentlyContinue)
}

# 1) Check git
if (-not (Check-Command git)) {
    Write-Host "Error: 'git' no encontrado. Instala Git antes de continuar." -ForegroundColor Red
    exit 1
}

# 2) Ensure working copy is clean
$st = git status --porcelain
if ($st) {
    if (-not $Force) {
        Write-Host "Tu working tree tiene cambios sin commitear. Haz commit o ejecuta con -Force para proseguir." -ForegroundColor Yellow
        git status -s
        exit 1
    } else {
        Write-Host "Forzando a pesar de cambios sin commitear..." -ForegroundColor Yellow
    }
}

# 3) Create remote if not present
$remotes = git remote
if (-not $remotes) {
    if ($RepoUrl) {
        git remote add origin $RepoUrl
        Write-Host "Remote 'origin' añadido: $RepoUrl"
    } elseif (Check-Command gh) {
        Write-Host "No hay remote. Creando repo en GitHub con 'gh repo create'..."
        gh repo create --public --source=. --remote=origin --push
    } else {
        Write-Host "No se encontró remote y gh no está instalado. Usa 'git remote add origin <url>' y ejecuta de nuevo." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Remote(s) existentes:" -NoNewline; git remote -v
}

# 4) Push main branch
git branch -M main
git push -u origin main
if ($LASTEXITCODE -ne 0) { Write-Host "Error al pushear la rama main" -ForegroundColor Red; exit 1 }

# 5) Create and push annotated tag
Write-Host "Creando tag $Version"
if (git tag -l | Select-String -Pattern "^$Version$") {
    Write-Host "Tag $Version ya existe." -ForegroundColor Yellow
    if (-not $Force) { Write-Host "Usa -Force para sobrescribir"; exit 1 }
    git tag -d $Version
}

git tag -a $Version -m "Release $Version"
git push origin $Version
if ($LASTEXITCODE -ne 0) { Write-Host "Error al pushear el tag" -ForegroundColor Red; exit 1 }

Write-Host "Tag $Version empujado. La workflow 'Build and Release Windows EXE' debería iniciarse automáticamente." -ForegroundColor Green
Write-Host "Verifica en: https://github.com/<tu-usuario>/<repo>/actions y en https://github.com/<tu-usuario>/<repo>/releases" -ForegroundColor Cyan

# Optionally watch the workflow with gh
if (Check-Command gh) {
    Write-Host "Si quieres, puedes seguir la ejecución con: gh run watch --repo $(git config --get remote.origin.url | sed 's/\.git$//; s/^.*github.com\///')"
}

Write-Host "Script finalizado." -ForegroundColor Green
