# 🚀 UwU-CLI User Guide

## 🎯 **What is UwU-CLI?**

UwU-CLI is a powerful, feature-rich command-line interface that integrates with Telegram for remote control and Cursor editor for AI-powered development assistance. It's designed to make your development workflow more efficient and fun!

## ✨ **Key Features**

- **🔧 Advanced CLI**: Enhanced command execution with autosuggestions
- **📱 Telegram Integration**: Remote control via Telegram bot
- **🤖 Cursor AI Integration**: Send AI prompts directly to Cursor
- **🛣️ Global Installation**: Run from anywhere in your terminal
- **🔒 Security**: Secure command execution with whitelisting
- **📊 State Management**: Persistent sessions and command history
- **🎨 Themes**: Customizable UI themes and effects

## 🚀 **Quick Start**

### **1. Installation**

#### **Windows**
```bash
# Run the setup script
.\setup_path.bat

# Or manually add to PATH
setx PATH "%PATH%;C:\path\to\UwU-Cli"
```

#### **PowerShell**
```powershell
# Run the setup script
.\setup_path.ps1
```

#### **Linux/macOS**
```bash
# Make executable and run
chmod +x setup_path.sh
./setup_path.sh
```

### **2. Configuration**

1. **Create `.autopilot.json`** in your project directory:
```json
{
  "enabled": true,
  "adapters": ["telegram"],
  "telegram": {
    "token": "YOUR_BOT_TOKEN",
    "chatId": "YOUR_CHAT_ID"
  }
}
```

2. **Get Telegram Bot Token**:
   - Message @BotFather on Telegram
   - Create a new bot with `/newbot`
   - Copy the token to `.autopilot.json`

3. **Get Chat ID**:
   - Send a message to your bot
   - Visit: `https://api.telegram.org/bot<TOKEN>/getUpdates`
   - Copy your chat ID from the response

### **3. First Run**

```bash
# Start UwU-CLI
uwu-cli

# Or from project directory
python uwu_cli.py
```

## 📱 **Telegram Remote Control**

### **Bot Commands**
- `/start` - Show welcome message
- `/help` - Comprehensive help
- `/status` - Check bot status
- `/commands` - List all commands
- `/security` - Security information

### **CLI Commands via Telegram**
Send any text to execute as a CLI command:
```
ls          → List files
pwd         → Show current directory
git status  → Check git status
help        → Show UwU-CLI help
```

### **Terminal Commands via Telegram**
Commands starting with `!` execute as terminal commands:
```
!dir        → List files (Windows)
!ls -la     → List files (Unix)
!git log    → Git history
!python --version → Python version
```

## 🤖 **Cursor AI Integration**

### **AI Chat Commands**
Use `cursor:cmd` to send prompts to Cursor's AI:

```
cursor:cmd 'continue'           → Continue writing code
cursor:cmd 'explain this'       → Explain selected code
cursor:cmd 'fix this bug'       → Help debug issues
cursor:cmd 'optimize this'      → Improve code performance
cursor:cmd 'add tests'          → Generate test code
```

### **How It Works**
1. **Send command** via Telegram or CLI
2. **Cursor activates** and opens AI chat panel
3. **Prompt is typed** automatically
4. **AI responds** in Cursor's chat panel
5. **You see results** in real-time

### **Cursor Shortcuts**
Use `cursor:shortcut` for keyboard shortcuts:
```
cursor:shortcut ctrl+s          → Save file
cursor:shortcut ctrl+f          → Find text
cursor:shortcut f5              → Start debugging
cursor:shortcut ctrl+shift+p    → Command palette
```

## 🔧 **Advanced CLI Features**

### **Command Aliases**
UwU-CLI automatically handles common command variations:
```
pwd, Pwd, PWD     → All work the same
ls, Ls, LS        → All work the same
clear, cls, Clear → All work the same
```

### **Enhanced Commands**
- **File Operations**: Enhanced `dir`/`ls` with colors and icons
- **Git Integration**: Built-in git command enhancements
- **Python Support**: Optimized Python command execution
- **Cross-Platform**: Works on Windows, macOS, and Linux

### **State Management**
- **Session Persistence**: Commands and context saved between sessions
- **Command History**: Access previous commands with up/down arrows
- **Working Directory**: Maintains current directory across commands
- **Preferences**: Customizable settings and themes

## 🎨 **Customization**

### **Themes**
Change the look and feel:
```
theme default      → Default theme
theme uwu          → UwU-themed colors
theme dark         → Dark mode
theme light        → Light mode
```

### **Auto-Clapback**
Enable automatic responses:
```
auto_clapback on   → Enable automatic responses
auto_clapback off  → Disable automatic responses
```

### **Plugins**
Extend functionality with plugins:
- Place `.py` files in the `plugins/` directory
- Plugins auto-load on startup
- Use `plugin:help` to see available plugins

## 🔒 **Security Features**

### **Command Whitelisting**
Only approved commands can execute:
- **File Operations**: `dir`, `ls`, `cd`, `pwd`
- **Git Commands**: `git status`, `git log`, `git diff`
- **Build Tools**: `npm install`, `python -m pip install`
- **Safe Commands**: `echo`, `whoami`, `date`

### **Path Restrictions**
Commands are restricted to safe directories:
- **Working Directory**: Only current project and subdirectories
- **System Protection**: No access to system directories
- **User Data Protection**: No access to user profile data

### **Output Sanitization**
Sensitive information is automatically masked:
- **API Keys**: Automatically detected and masked
- **Passwords**: Hidden from output
- **File Paths**: Sanitized for security
- **User Information**: Protected from exposure

## 🚨 **Troubleshooting**

### **Common Issues**

#### **Telegram Bot Not Responding**
- Check if UwU-CLI is running
- Verify token and chat ID in `.autopilot.json`
- Check internet connection
- Restart UwU-CLI

#### **Cursor Commands Not Working**
- Ensure Cursor is open and visible
- Check if Cursor is in focus
- Install pywin32: `pip install pywin32`
- Try manual method: `Ctrl+Shift+I` then type prompt

#### **Global Command Not Found**
- Restart terminal after running setup script
- Check PATH environment variable
- Run setup script from UwU-CLI directory
- Verify global launcher was created

#### **Permission Errors**
- Run as administrator (Windows)
- Check file permissions (Linux/macOS)
- Verify Python installation
- Check antivirus software

### **Debug Mode**
Enable detailed logging:
```python
# In uwu_cli.py, change logging level
logging.basicConfig(level=logging.DEBUG)
```

### **Reset Configuration**
Delete configuration files to reset:
```bash
# Remove autopilot config
rm .autopilot.json

# Remove state files
rm -rf tmp/
```

## 📚 **Command Reference**

### **Core Commands**
```
help                    → Show help
exit, quit             → Exit UwU-CLI
clear, cls             → Clear screen
theme <name>           → Change theme
auto_clapback <on/off> → Toggle auto-responses
```

### **File Operations**
```
pwd                     → Show current directory
ls, dir                → List files
cd <directory>         → Change directory
```

### **Cursor Integration**
```
cursor:help            → Show Cursor commands
cursor:status          → Check Cursor availability
cursor:open <file>     → Open file in Cursor
cursor:cmd <prompt>    → Send AI prompt to Cursor
cursor:shortcut <key>  → Send keyboard shortcut
```

### **Telegram Control**
```
telegram:start         → Start Telegram control
telegram:stop          → Stop Telegram control
telegram:status        → Check Telegram status
```

## 🎯 **Best Practices**

### **Daily Workflow**
1. **Start UwU-CLI** in your project directory
2. **Use Telegram** for remote commands
3. **Integrate with Cursor** for AI assistance
4. **Leverage aliases** for efficiency
5. **Save sessions** for continuity

### **Security Guidelines**
- **Never share** your `.autopilot.json` file
- **Use strong** bot tokens
- **Limit access** to trusted users only
- **Monitor logs** for suspicious activity
- **Keep updated** with latest security patches

### **Performance Tips**
- **Cache responses** for repeated commands
- **Use aliases** for common operations
- **Batch commands** when possible
- **Monitor memory** usage
- **Clean up** old session data

## 🚀 **Advanced Usage**

### **Scripting**
Use UwU-CLI in scripts:
```bash
#!/bin/bash
echo "ls" | uwu-cli
echo "git status" | uwu-cli
```

### **API Integration**
Access UwU-CLI programmatically:
```python
from uwu_cli import UwUCLI

cli = UwUCLI()
result = cli.shell_command("ls")
print(result)
```

### **Plugin Development**
Create custom plugins:
```python
# plugins/my_plugin.py
def register(cli):
    return {
        "on_start": lambda: print("Plugin loaded!"),
        "commands": {"custom": lambda: "Custom command!"}
    }
```

## 📞 **Support & Community**

### **Getting Help**
- **Documentation**: Check this guide first
- **Issues**: Report bugs on GitHub
- **Discussions**: Join community discussions
- **Examples**: Check the examples directory

### **Contributing**
- **Fork** the repository
- **Create** a feature branch
- **Make** your changes
- **Test** thoroughly
- **Submit** a pull request

### **Resources**
- **GitHub**: [UwU-CLI Repository](https://github.com/your-repo)
- **Documentation**: [Full Documentation](https://docs.uwu-cli.dev)
- **Discord**: [Community Server](https://discord.gg/uwu-cli)
- **Blog**: [Latest Updates](https://blog.uwu-cli.dev)

---

**🎉 Congratulations!** You're now ready to use UwU-CLI like a pro!

**Stay sparkly~ ✨** and happy coding! 🚀 