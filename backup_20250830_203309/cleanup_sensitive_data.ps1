# PowerShell script to clean sensitive data from git history
# Based on the comprehensive cleanup plan from ChatGPT

Write-Host "🚨 UwU-CLI Sensitive Data Cleanup Script" -ForegroundColor Red
Write-Host "=============================================" -ForegroundColor Red

# Step 1: Create a backup of the current state
Write-Host "`n[1/8] Creating backup of current state..." -ForegroundColor Yellow
$backupDir = "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
Copy-Item -Path ".\*" -Destination $backupDir -Recurse -Force -Exclude ".git", "backup_*"
Write-Host "✅ Backup created in: $backupDir" -ForegroundColor Green

# Step 2: Check if we're in a git repository
Write-Host "`n[2/8] Verifying git repository..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    Write-Host "❌ Not a git repository. Exiting." -ForegroundColor Red
    exit 1
}
Write-Host "✅ Git repository confirmed" -ForegroundColor Green

# Step 3: Check for sensitive files in history
Write-Host "`n[3/8] Scanning git history for sensitive files..." -ForegroundColor Yellow
$sensitiveFiles = @()

# Check for .autopilot.json
$autopilotLog = git log --all --name-only -- .autopilot.json 2>$null
if ($autopilotLog) {
    $sensitiveFiles += ".autopilot.json"
    Write-Host "⚠️  Found .autopilot.json in history" -ForegroundColor Yellow
}

# Check for .env
$envLog = git log --all --name-only -- .env 2>$null
if ($envLog) {
    $sensitiveFiles += ".env"
    Write-Host "⚠️  Found .env in history" -ForegroundColor Yellow
}

# Check for other potential sensitive files
$otherSensitive = git log --all --name-only | Select-String -Pattern "\.(key|pem|p12|pfx|crt|config)$" | ForEach-Object { $_.ToString().Trim() }
if ($otherSensitive) {
    $sensitiveFiles += $otherSensitive
    Write-Host "⚠️  Found other potentially sensitive files in history" -ForegroundColor Yellow
}

if ($sensitiveFiles.Count -eq 0) {
    Write-Host "✅ No sensitive files found in git history" -ForegroundColor Green
} else {
    Write-Host "❌ Found $($sensitiveFiles.Count) sensitive files in history" -ForegroundColor Red
    $sensitiveFiles | ForEach-Object { Write-Host "   - $_" -ForegroundColor Red }
}

# Step 4: Create replacements file for inline secrets
Write-Host "`n[4/8] Creating replacements file for inline secrets..." -ForegroundColor Yellow
$replacementsContent = @"
# Replacements file for git-filter-repo
# Format: PLAINTEXT or regex:... ==>REPLACEMENT

# OpenRouter API key
regex:(?i)sk-or-v1-[A-Za-z0-9_\-]{20,}==>REMOVED

# GitHub PAT
regex:ghp_[A-Za-z0-9]{20,}==>REMOVED

# Telegram bot token
regex:\d{6,}:[A-Za-z0-9_\-]{30,}==>REMOVED

# JWTs
regex:eyJ[A-Za-z0-9_\-]+?\.[A-Za-z0-9_\-]+?\.[A-Za-z0-9_\-]+==>REMOVED

# AWS Access Key ID
regex:AKIA[0-9A-Z]{16}==>REMOVED

# Generic .env style lines
regex:(?i)(OPENROUTER_API_KEY\s*[:=]\s*)\S+==>$1REMOVED
regex:(?i)(SMTP_PASSWORD\s*[:=]\s*)\S+==>$1REMOVED
regex:(?i)(FEISHU_APP_SECRET\s*[:=]\s*)\S+==>$1REMOVED
regex:(?i)(TELEGRAM_BOT_TOKEN\s*[:=]\s*)\S+==>$1REMOVED
regex:(?i)(API_KEY\s*[:=]\s*)\S+==>$1REMOVED
regex:(?i)(SECRET\s*[:=]\s*)\S+==>$1REMOVED
regex:(?i)(TOKEN\s*[:=]\s*)\S+==>$1REMOVED
"@

$replacementsContent | Out-File -FilePath "replacements.txt" -Encoding UTF8
Write-Host "✅ Replacements file created: replacements.txt" -ForegroundColor Green

# Step 5: Use git-filter-repo to clean history
Write-Host "`n[5/8] Cleaning sensitive files from git history..." -ForegroundColor Yellow

# Remove sensitive files from all history
if ($sensitiveFiles.Count -gt 0) {
    $filterArgs = @("--sensitive-data-removal", "--invert-paths")
    foreach ($file in $sensitiveFiles) {
        $filterArgs += "--path", $file
    }
    
    Write-Host "Running: git filter-repo $($filterArgs -join ' ')" -ForegroundColor Cyan
    & git filter-repo @filterArgs
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Sensitive files removed from history" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to remove sensitive files from history" -ForegroundColor Red
        Write-Host "Continuing with inline secret cleanup..." -ForegroundColor Yellow
    }
} else {
    Write-Host "✅ No sensitive files to remove from history" -ForegroundColor Green
}

# Step 6: Clean inline secrets
Write-Host "`n[6/8] Cleaning inline secrets from git history..." -ForegroundColor Yellow
Write-Host "Running: git filter-repo --sensitive-data-removal --replace-text replacements.txt" -ForegroundColor Cyan
& git filter-repo --sensitive-data-removal --replace-text replacements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Inline secrets cleaned from history" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to clean inline secrets from history" -ForegroundColor Red
}

# Step 7: Verify cleanup
Write-Host "`n[7/8] Verifying cleanup..." -ForegroundColor Yellow

# Check if sensitive files still exist in history
$remainingAutopilot = git log --all -- .autopilot.json 2>$null
$remainingEnv = git log --all -- .env 2>$null

if (-not $remainingAutopilot -and -not $remainingEnv) {
    Write-Host "✅ Sensitive files successfully removed from history" -ForegroundColor Green
} else {
    Write-Host "❌ Some sensitive files still exist in history" -ForegroundColor Red
    if ($remainingAutopilot) { Write-Host "   - .autopilot.json still exists" -ForegroundColor Red }
    if ($remainingEnv) { Write-Host "   - .env still exists" -ForegroundColor Red }
}

# Step 8: Final instructions
Write-Host "`n[8/8] Cleanup complete!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

Write-Host "`n📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Review the changes above" -ForegroundColor White
Write-Host "2. Force push to remote: git push --force --all" -ForegroundColor White
Write-Host "3. Force push tags: git push --force --tags" -ForegroundColor White
Write-Host "4. Contact GitHub Support to purge cached diffs if needed" -ForegroundColor White
Write-Host "5. Rotate any exposed API keys/tokens" -ForegroundColor White
Write-Host "6. Update .gitignore to prevent future commits of sensitive files" -ForegroundColor White

Write-Host "`n⚠️  IMPORTANT: This script has rewritten git history!" -ForegroundColor Red
Write-Host "   All collaborators must re-clone the repository." -ForegroundColor Red
Write-Host "   Backup is available in: $backupDir" -ForegroundColor Yellow

Write-Host "`n🔒 Security recommendations:" -ForegroundColor Cyan
Write-Host "- Enable GitHub Secret Scanning" -ForegroundColor White
Write-Host "- Enable Push Protection" -ForegroundColor White
Write-Host "- Use environment variables for secrets" -ForegroundColor White
Write-Host "- Add .env and .autopilot.json to .gitignore" -ForegroundColor White