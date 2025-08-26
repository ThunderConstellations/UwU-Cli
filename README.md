# 🚀 UwU-CLI: Professional-Grade Development Shell with AI Assistance

[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)](https://github.com/ThunderConstellations/UwU-Cli/releases)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/ThunderConstellations/UwU-Cli)

**UwU-CLI** is a revolutionary command-line interface that transforms your terminal into a professional-grade development environment with AI assistance capabilities. Built for developers who want the power of modern AI tools integrated seamlessly into their workflow.

## ✨ Features

### 🔄 Infinite AI Assistance Mode

- **Continuous AI assistance** until task completion
- **Context persistence** across sessions
- **Smart task detection** and continuation
- **Plan tracking** and reference management

### 💻 Multi-Shell Command Routing

- **`cmd:`** - Execute commands in CMD shell
- **`ps1:`** - Execute commands in PowerShell
- **`bash:`** - Execute commands in Bash (if available)
- **`cs:`** - Quick Cursor AI commands
- **Intelligent routing** with output capture

### 🔬 Advanced Research Modes

- **`deep:`** - Deep research with comprehensive analysis
- **`review:`** - Code review for systematic error detection
- **`audit:`** - Full project audit and analysis
- **Enhanced AI prompts** for thorough research

### 🚀 Enhanced Quick Commands

- **`/e`** - Explain code + create comprehensive documentation
- **`/p`** - Research + plan + create project roadmap
- **`/cc`** - Continue where left off with context awareness
- **`/c`, `/f`, `/o`, `/t`, `/r`, `/d`, `/h`, `/s`, `/g`** - Standard commands

### 🤖 Intelligent Command Routing

- **AI chat detection** and automatic routing
- **Shell command routing** to appropriate environments
- **Context-aware processing** for optimal results
- **Enhanced error handling** and recovery

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Windows, macOS, or Linux
- Cursor IDE (optional, for enhanced features)

### Installation

#### Windows (Recommended)
```batch
# Clone the repository
git clone https://github.com/ThunderConstellations/UwU-Cli.git
cd UwU-Cli

# Run the installer (as Administrator)
install.bat

# Start UwU-CLI
uwu
```

#### PowerShell
```powershell
# Clone the repository
git clone https://github.com/ThunderConstellations/UwU-Cli.git
cd UwU-Cli

# Run the installer (as Administrator)
.\install.ps1

# Start UwU-CLI
uwu
```

#### Unix/Linux/macOS

```bash
# Make executable and run
chmod +x install.sh
./install.sh
```

#### Manual Installation

```bash
# Clone the repository
git clone https://github.com/ThunderConstellations/UwU-Cli.git
cd UwU-Cli

# Install in development mode
pip install -e .

# Start UwU-CLI
python uwu_cli.py
```

### Usage

After installation, you can run UwU-CLI from anywhere:

```bash
# Start UwU-CLI
uwu-cli

# Or use the short command
uwu
```

## 🎮 Command Reference

### Infinite Mode Commands

```bash
/infiniteon          # Enable continuous AI assistance
/infiniteoff         # Disable infinite mode
/infinite            # Show infinite mode status
```

### Multi-Shell Commands

```bash
cmd:dir              # Execute in CMD shell
ps1:Get-Process      # Execute in PowerShell
bash:ls -la          # Execute in Bash
cs:explain this      # Send to Cursor AI
```

### Research Modes

```bash
deep:python optimization     # Deep research mode
review:main.py               # Code review mode
audit:src/                   # Full project audit
```

### Enhanced Quick Commands

```bash
/e                           # Explain code + create .md
/p                           # Research + plan + .md
/cc                          # Continue where left off
```

## 🏗️ Architecture

UwU-CLI is built with a modular architecture:

- **Core CLI Engine** - Command processing and routing
- **AI Integration** - Cursor IDE and conversation management
- **State Management** - Session persistence and configuration
- **Plugin System** - Extensible command architecture
- **Multi-Shell Support** - Cross-platform shell integration

## 🔧 Configuration

Configuration files are stored in the `config/` directory:

- `main.json` - Main configuration settings
- `telegram.json` - Telegram bot configuration
- `security.json` - Security and authentication settings
- `performance.json` - Performance optimization settings

## 📱 Telegram Integration

UwU-CLI includes remote control capabilities via Telegram:

```bash
telegram:start        # Start remote control
telegram:stop         # Stop remote control
telegram:status       # Check remote control status
telegram:enable       # Enable Telegram control
telegram:disable      # Disable Telegram control
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Test all advanced features
python test_advanced_features.py

# Test specific components
python test_cursor_cmd_fix.py
```

## 🚀 Advanced Features

### AI Conversation Management

- **Persistent storage** of AI conversations
- **Conversation history** and search
- **Export functionality** for external use
- **Statistics tracking** and analytics

### Performance Optimizations

- **Lazy loading** of components
- **Smart caching** system
- **Memory management** optimization
- **Background processing** support

### Cross-Platform Support

- **Windows** - Full CMD and PowerShell integration
- **macOS** - Native shell support
- **Linux** - Bash and shell integration
- **Unified interface** across platforms

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone and setup development environment
git clone https://github.com/ThunderConstellations/UwU-Cli.git
cd UwU-Cli
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test files
python test_advanced_features.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Cursor IDE** for AI integration capabilities
- **Python community** for excellent libraries and tools
- **Open source contributors** for inspiration and code

## 📞 Support & Community

- **Issues**: [GitHub Issues](https://github.com/ThunderConstellations/UwU-Cli/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ThunderConstellations/UwU-Cli/discussions)
- **Documentation**: [Wiki](https://github.com/ThunderConstellations/UwU-Cli/wiki)

## 🎯 Roadmap

- [ ] Auto-suggestions system
- [ ] Syntax highlighting and formatting
- [ ] Plugin marketplace
- [ ] Multi-modal AI integration
- [ ] Cloud platform integration
- [ ] Advanced Git workflow automation

---

**Made with ❤️ by the UwU-CLI Team**

_Transform your terminal into an AI-powered development powerhouse!_
