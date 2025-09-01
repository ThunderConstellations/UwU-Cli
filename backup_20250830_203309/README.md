# 🐱 UwU-CLI - The Ultimate Chaotic CMD Replacement

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://t.me/)
[![Cursor IDE](https://img.shields.io/badge/Cursor-IDE-purple.svg)](https://cursor.sh/)

> A fully-featured, AI-powered, context-aware CMD replacement that combines the functionality of CMD with Clink autosuggestions, chaotic UwU energy, automatic clapbacks, and AI assistance.

## 🚀 **Quick Start**

### **Installation**

```bash
# Clone the repository
git clone https://github.com/ThunderConstellations/UwU-Cli.git
cd UwU-Cli

# Install dependencies
pip install -r requirements.txt

# Run UwU-CLI
python uwu_cli.py
```

### **Global Installation (Windows)**

```batch
# Run as administrator
install_uwu_cli.bat
```

### **Global Installation (PowerShell)**

```powershell
# Run as administrator
.\install_uwu_cli.ps1
```

## 🎯 **Core Features**

### **🤖 AI-Powered Development**
- **Cursor AI Integration** - Seamless AI assistance in your terminal
- **OpenRouter Support** - Multiple AI models and reasoning capabilities
- **Context Awareness** - AI remembers your project context
- **Infinite Mode** - Continuous AI assistance until task completion

### **📱 Remote Control via Telegram**
- **17 Quick Commands** - Short, efficient commands for common tasks
- **Multi-Shell Routing** - Execute commands in CMD, PowerShell, Bash
- **Research Modes** - Deep research, code review, security audit
- **Real-time Updates** - Get AI responses and command results instantly

### **🔧 Professional Shell Experience**
- **Oh-my-zsh Parity** - Professional appearance and functionality
- **Advanced Autosuggestions** - Smart command completion
- **Theme System** - Customizable prompts and appearance
- **Plugin Ecosystem** - Extensible architecture for community contributions

## 📚 **Documentation & Rules**

### **Cursor Rules Integration**
This project uses [Cursor IDE](https://cursor.sh/) with comprehensive rules for consistent development:

- **`.cursor/rules/uwu-cli-rules.mdc`** - Master rules for UwU-CLI development
- **`.cursor/rules/senior.mdc`** - Senior developer standards and best practices
- **`.cursor/rules/clean-code.mdc`** - Clean code guidelines and principles
- **`.cursor/rules/code-analysis.mdc`** - Code analysis and quality tools
- **`.cursor/rules/mcp.mdc`** - MCP server usage guidelines
- **`.cursor/rules/mermaid.mdc`** - Diagram generation for documentation
- **`.cursor/rules/task-list.mdc`** - Task management and tracking
- **`.cursor/rules/add-to-changelog.mdc`** - Changelog management
- **`.cursor/rules/after_each_chat.mdc`** - Chat session management
- **`.cursor/rules/10x-tool-call.mdc`** - Automated task progression
- **`.cursor/rules/pineapple.mdc`** - Special development modes
- **`.cursor/rules/better-auth-react-standards.mdc`** - Authentication standards

### **Key Documentation Files**
- **`USER_GUIDE.md`** - Comprehensive user guide
- **`ENHANCED_FEATURES_SUMMARY.md`** - Latest feature documentation
- **`CHANGELOG.md`** - Complete version history
- **`TASKS.md`** - Current development tasks
- **`PROJECT_STATUS.md`** - Overall project status

## 🎮 **Quick Commands Reference**

### **Core Commands**
| Command | Description |
|---------|-------------|
| `/c` | Continue improving and ensure quick commands work |
| `/e` | Explain code and show example usage |
| `/p` | Research and plan issues and improvements |
| `/cc` | Continue from where previous session left off |

### **Streamlined Commands**
| Command | Description |
|---------|-------------|
| `/cs` | Continue as planned |
| `/f` | Fix any issues found |
| `/o` | Optimize code for performance |
| `/t` | Test functionality thoroughly |
| `/r` | Review code for improvements |
| `/d` | Debug issues step by step |
| `/h` | Help understanding |
| `/s` | Show current status |
| `/g` | Generate solutions |

### **Infinite Mode Commands**
| Command | Description |
|---------|-------------|
| `/infinite` | Continue working until completion |
| `/infiniteon` | Start infinite mode |
| `/infiniteoff` | Stop infinite mode |
| `/help` | Show all available commands |

## 🔌 **Multi-Shell Commands**

Execute commands in specific shells:

```bash
# Windows CMD
cmd: echo Hello from CMD

# PowerShell
ps1: Write-Host "Hello from PowerShell"

# Bash (WSL on Windows)
bash: echo "Hello from Bash"

# Cursor AI
cs: continue working on this project
```

## 🔍 **Research Mode Commands**

Specialized AI assistance modes:

```bash
# Deep research
deep: improve this codebase

# Code review
review: analyze this code

# Security audit
audit: check for security issues
```

## 🏗️ **Project Structure**

```
UwU-Cli/
├── .cursor/rules/           # Cursor IDE development rules
├── config/                  # Configuration files
├── phrases/                 # Roast phrases and content
├── plugins/                 # Plugin system
├── scripts/                 # Utility scripts
├── tests/                   # Test suite
├── tmp/                     # Temporary files and logs
├── tts/                     # Text-to-speech functionality
├── utils/                   # Core utilities
├── uwu_cli.py              # Main CLI application
├── uwu.py                   # Alternative entry point
├── requirements.txt         # Python dependencies
├── setup.py                 # Package configuration
└── README.md               # This file
```

## ⚙️ **Configuration**

### **Main Configuration**
```json
{
  "telegram_enabled": true,
  "cursor_integration": true,
  "ai_provider": "openrouter",
  "theme": "uwu",
  "auto_clapback": true
}
```

### **Environment Variables**
```bash
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# OpenRouter AI
OPENROUTER_API_KEY=your_api_key

# Cursor IDE
CURSOR_AGENT_PATH=/path/to/cursor-agent
```

## 🧪 **Testing**

### **Run All Tests**
```bash
python test_enhanced_features.py
```

### **Run Specific Test Categories**
```bash
# Test quick commands
python test_quick_commands.py

# Test CLI functionality
python test_cli_commands.py

# Test Cursor integration
python test_cursor_enhancements.py
```

## 🚀 **Advanced Usage**

### **Infinite Mode**
Start continuous AI assistance for complex tasks:

```bash
# Start infinite mode
/infiniteon "Implement user authentication system"

# Check status
/status

# Stop when complete
/infiniteoff
```

### **Custom Themes**
Create and use custom themes:

```python
# In your config
{
  "theme": "custom",
  "custom_theme": {
    "prompt_color": "cyan",
    "error_color": "red",
    "success_color": "green"
  }
}
```

### **Plugin Development**
Create custom plugins:

```python
# Example plugin
class MyPlugin:
    def uwu_command_suggestions(self, context: str) -> List[str]:
        return ["custom_command1", "custom_command2"]
    
    def uwu_toolbar(self) -> List[ToolbarItem]:
        return [ToolbarItem("Custom Tool", "custom_action")]
```

## 🔒 **Security Features**

- **Command Whitelisting** - Secure command execution
- **PTY-based Execution** - No shell=True vulnerabilities
- **Input Validation** - Sanitized command processing
- **Timeout Protection** - Prevents hanging commands
- **Secret Redaction** - Protects sensitive information

## 🌟 **Contributing**

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### **Development Setup**
```bash
# Clone and setup
git clone https://github.com/ThunderConstellations/UwU-Cli.git
cd UwU-Cli

# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Follow our coding standards
# See .cursor/rules/ for development guidelines
```

### **Code Standards**
- Follow the rules in `.cursor/rules/`
- Use clean code principles (see `.cursor/rules/clean-code.mdc`)
- Maintain test coverage
- Follow semantic versioning

## 📈 **Roadmap**

### **Version 2.3.0 (Next)**
- [ ] Rich theming system with Starship integration
- [ ] Advanced autosuggestions with ML
- [ ] Plugin marketplace
- [ ] Performance optimizations

### **Version 2.4.0 (Future)**
- [ ] Feishu and Gmail connectors
- [ ] Advanced Cursor rules management
- [ ] Community plugin ecosystem
- [ ] Cross-platform shell integration

## 🐛 **Troubleshooting**

### **Common Issues**

**Telegram Bot Not Responding**
```bash
# Check configuration
cat .autopilot.json

# Verify bot token
echo $TELEGRAM_BOT_TOKEN
```

**Cursor AI Integration Issues**
```bash
# Test Cursor connection
python -c "from utils.cursor_controller import get_cursor_controller; print('Cursor working')"
```

**Quick Commands Not Working**
```bash
# Test quick commands
python test_quick_commands.py

# Check command definitions
python -c "from uwu_cli import UwUCLI; cli = UwUCLI(); print(cli.get_quick_commands_help())"
```

### **Getting Help**
- **Documentation**: Check `USER_GUIDE.md` and `ENHANCED_FEATURES_SUMMARY.md`
- **Issues**: [GitHub Issues](https://github.com/ThunderConstellations/UwU-Cli/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ThunderConstellations/UwU-Cli/discussions)

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Cursor IDE** - For the amazing AI-powered development experience
- **OpenRouter** - For providing access to multiple AI models
- **Python Community** - For the excellent libraries and tools
- **Open Source Contributors** - For making this project possible

## 🌟 **Star History**

[![Star History Chart](https://api.star-history.com/svg?repos=ThunderConstellations/UwU-Cli&type=Date)](https://star-history.com/#ThunderConstellations/UwU-Cli&Date)

---

**Made with ❤️ and 🐱 by the UwU-CLI Team**

*Stay wavy~ nyah x3*
