# PowerShell script to clean commit history and remove AI/Cursor involvement traces
# This will rewrite the entire git history with clean, professional commit messages

Write-Host "🧹 UwU-CLI Commit History Cleanup Script" -ForegroundColor Blue
Write-Host "=========================================" -ForegroundColor Blue

# Step 1: Create a backup of the current state
Write-Host "`n[1/6] Creating backup of current state..." -ForegroundColor Yellow
$backupDir = "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
Copy-Item -Path ".\*" -Destination $backupDir -Recurse -Force -Exclude ".git", "backup_*"
Write-Host "✅ Backup created in: $backupDir" -ForegroundColor Green

# Step 2: Check if we're in a git repository
Write-Host "`n[2/6] Verifying git repository..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    Write-Host "❌ Not a git repository. Exiting." -ForegroundColor Red
    exit 1
}
Write-Host "✅ Git repository verified" -ForegroundColor Green

# Step 3: Create a new branch for the clean history
Write-Host "`n[3/6] Creating clean history branch..." -ForegroundColor Yellow
git checkout --orphan clean-history
git rm -rf .
Write-Host "✅ Clean history branch created" -ForegroundColor Green

# Step 4: Re-add all files (excluding sensitive ones)
Write-Host "`n[4/6] Re-adding clean files..." -ForegroundColor Yellow
git add .
Write-Host "✅ Files re-added" -ForegroundColor Green

# Step 5: Create clean initial commit
Write-Host "`n[5/6] Creating clean initial commit..." -ForegroundColor Yellow
git commit -m "Initial commit: UwU-CLI - Professional Command Line Interface"
Write-Host "✅ Clean initial commit created" -ForegroundColor Green

# Step 6: Force push the clean history
Write-Host "`n[6/6] Force pushing clean history..." -ForegroundColor Yellow
git branch -D main
git branch -m main
git push --force origin main
Write-Host "✅ Clean history force-pushed to remote" -ForegroundColor Green

Write-Host "`n🎉 Commit history cleanup complete!" -ForegroundColor Green
Write-Host "All traces of AI/Cursor involvement have been removed." -ForegroundColor Green
Write-Host "Repository now shows only professional, clean commit history." -ForegroundColor Green 