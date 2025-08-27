# 🔒 Security Guide for UwU-CLI

## ⚠️ IMPORTANT: Protect Your Sensitive Information

UwU-CLI uses various APIs and services that require authentication tokens, API keys, and passwords. **NEVER commit these to version control or share them publicly.**

## 🚨 Files That Contain Sensitive Information

The following files contain sensitive information and are **automatically excluded** from Git:

- `.autopilot.json` - Contains API keys, tokens, and passwords
- `.telegram_config.json` - Contains Telegram bot tokens
- `*.config.json` - Any configuration files with secrets
- `*.auth.json` - Authentication files
- `*.secret.json` - Secret files
- `*.key.json` - API key files
- `*.token.json` - Token files
- `*.password.json` - Password files
- `.env*` - Environment variable files
- `session.json` - Session data
- `context.json` - Context data
- `preferences.json` - User preferences

## 🔐 Setting Up Your Configuration

### 1. Copy the Template
```bash
# Copy the template file
cp .autopilot.json.template .autopilot.json

# Edit with your actual credentials
notepad .autopilot.json  # Windows
nano .autopilot.json     # Linux/macOS
```

### 2. Fill in Your Credentials
Replace the placeholder values with your actual credentials:

```json
{
  "telegram": {
    "token": "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz",  // Your bot token
    "chatId": "123456789"                               // Your chat ID
  },
  "email": {
    "user": "your.email@gmail.com",                     // Your email
    "pass": "your-app-password"                         // Your app password
  }
}
```

### 3. Verify Git Ignore
Make sure these files are not tracked by Git:

```bash
git status
```

You should **NOT** see any of the sensitive files listed above.

## 🛡️ Security Best Practices

### 1. Use Environment Variables (Recommended)
Instead of storing secrets in JSON files, use environment variables:

```bash
# Windows
set TELEGRAM_TOKEN=your_token_here
set TELEGRAM_CHAT_ID=your_chat_id_here

# Linux/macOS
export TELEGRAM_TOKEN=your_token_here
export TELEGRAM_CHAT_ID=your_chat_id_here
```

### 2. Use .env Files (Alternative)
Create a `.env` file (automatically ignored by Git):

```bash
# .env
TELEGRAM_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
EMAIL_PASSWORD=your_password_here
```

### 3. Never Share Credentials
- ❌ Don't share API keys in chat
- ❌ Don't include them in screenshots
- ❌ Don't paste them in public forums
- ❌ Don't commit them to public repositories

### 4. Rotate Credentials Regularly
- Change passwords every 90 days
- Rotate API keys monthly
- Use app-specific passwords for email

## 🔍 Checking for Exposed Secrets

### 1. Git History Check
If you accidentally committed secrets, check your Git history:

```bash
git log --all --full-history -- .autopilot.json
```

### 2. Search for Secrets
Search your repository for common secret patterns:

```bash
# Search for API keys
git grep -n "AIza[0-9A-Za-z-_]{35}"

# Search for tokens
git grep -n "[0-9]{10}:[0-9A-Za-z_-]{35}"

# Search for email addresses
git grep -n "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
```

### 3. Use Git Hooks
Install pre-commit hooks to prevent accidental commits:

```bash
pip install pre-commit
pre-commit install
```

## 🚨 If You Accidentally Expose Secrets

### 1. Immediate Actions
- **IMMEDIATELY** revoke/rotate the exposed credentials
- Remove the file from Git tracking
- Check if the repository is public

### 2. Remove from Git History
```bash
# Remove file from Git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .autopilot.json" \
  --prune-empty --tag-name-filter cat -- --all

# Force push to remove from remote
git push origin --force --all
```

### 3. Notify Affected Services
- Contact the service provider
- Explain the security incident
- Request immediate credential rotation

## 📋 Security Checklist

Before pushing to GitHub, verify:

- [ ] `.autopilot.json` is not tracked by Git
- [ ] `.env` files are not tracked by Git
- [ ] No API keys in commit messages
- [ ] No passwords in code comments
- [ ] Configuration templates are properly sanitized
- [ ] Sensitive files are in `.gitignore`

## 🆘 Getting Help

If you have security concerns:

1. **Don't panic** - security issues can be resolved
2. **Act quickly** - rotate credentials immediately
3. **Document everything** - keep records of what was exposed
4. **Learn from mistakes** - implement better security practices

## 🔗 Additional Resources

- [GitHub Security Best Practices](https://docs.github.com/en/github/security)
- [Python Security Best Practices](https://docs.python-guide.org/security/)
- [Environment Variables Best Practices](https://12factor.net/config)

---

**Remember: Security is everyone's responsibility. When in doubt, keep it confidential!** 🔒 