# UwU-CLI: The Ultimate Chaotic CMD Replacement 💀

A fully-featured, AI-powered, context-aware CMD replacement that combines the functionality of CMD with Clink autosuggestions, chaotic UwU energy, automatic clapbacks, and AI assistance.

## 🌟 Features

### 🖥️ **Enhanced CMD Replacement**

- **Full CMD Compatibility** - All standard Windows CMD commands work
- **Command Aliases** - `ls` → `dir`, `clear` → `cls`, and more
- **Enhanced Output** - Colorful, themed command results
- **Autosuggestions** - Tab completion for commands and files
- **Command History** - Persistent command history with search

### 🤖 **AI Integration**

- **OpenRouter API** - Powered by DeepSeek R1 0528 (free model)
- **Smart Commands** - `ai:script`, `ai:cmd`, `ai:explain`, `ai:debug`, `ai:optimize`
- **Context-Aware** - AI understands your code and provides relevant assistance
- **Background Processing** - Non-blocking AI job queue

### 🎨 **Toxic Themes & UI**

- **Colorful Prompts** - Oh-My-Zsh style themes (toxic, rainbow, neon, pastel)
- **ASCII Effects** - Thunderbolts, bubble parties, psychic glows, wizard hats
- **Animated Spinners** - Loading animations with themed effects
- **Auto-Clapbacks** - Automatic toxic responses after every command

### 🔌 **Plugin System**

- **Extensible Architecture** - Easy to add new commands and features
- **Sample Plugins** - Git enhancer, development tools, and more
- **Hot Reloading** - Plugins load automatically without restart

### 🎯 **Productivity Features**

- **Smart Context Detection** - Automatically detects project types and frameworks
- **Command Chaining** - Pipe commands together for complex operations
- **Custom Aliases** - Create your own command shortcuts
- **Environment Management** - Easy configuration and customization

## 🚀 Quick Start

### Windows Installation

```batch
# Clone the repository
git clone https://github.com/ThunderConstellations/UwU-Cli.git
cd UwU-Cli

# Run the installer
installer.bat

# Start UwU-CLI
uwu
```

### Linux/macOS Installation

```bash
# Clone the repository
git clone https://github.com/ThunderConstellations/UwU-Cli.git
cd UwU-Cli

# Run the installer
chmod +x installer.sh
./installer.sh

# Start UwU-CLI
uwu
```

### Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Copy .env.example to .env and add your OpenRouter API key
cp env.example .env

# Start UwU-CLI
python uwu_cli.py
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# OpenRouter API Configuration
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=deepseek/deepseek-r1-0528:free
OPENROUTER_BASE_URL=https://api.openrouter.ai/v1

# AI Configuration
AI_ENABLED=true
AI_TIMEOUT=30
AI_MAX_TOKENS=1000
AI_TEMPERATURE=0.9

# Theme Configuration
DEFAULT_THEME=toxic
AUTO_CLAPBACK=true
```

### Get Your Free API Key

1. Visit [OpenRouter](https://openrouter.ai/keys)
2. Sign up for a free account
3. Generate an API key
4. Add it to your `.env` file

## 🎮 Basic Commands

### Shell Commands

```bash
dir          # Enhanced directory listing with icons
ls           # Alias for dir (Unix compatibility)
cd           # Change directory
cls          # Clear screen
help         # Show available commands
```

### AI Commands

```bash
ai:script "create a Python web scraper"    # Generate scripts
ai:cmd "list all files in current directory"  # Convert to CMD
ai:explain "git merge conflict"             # Get explanations
ai:debug "Python import error"              # Debug assistance
ai:optimize "slow database query"           # Optimization tips
```

### Theme Commands

```bash
theme toxic      # Switch to toxic theme
theme rainbow    # Switch to rainbow theme
theme neon       # Switch to neon theme
theme pastel     # Switch to pastel theme
```

### Plugin Commands

```bash
plugin list      # List available plugins
plugin enable git_enhancer  # Enable Git plugin
plugin help git_enhancer    # Show plugin help
```

## 🔧 Advanced Usage

### Custom Aliases

```bash
# Create custom command shortcuts
alias ll="dir /w"
alias update="git pull && pip install -r requirements.txt"
alias dev="python -m http.server 8000"
```

### Command Chaining

```bash
# Chain commands together
dir | findstr ".py" | sort
git status && git add . && git commit -m "Updates"
```

### Plugin Development

Create custom plugins in the `plugins/` directory:

```python
class MyPlugin:
    def __init__(self):
        self.name = "My Plugin"
        self.commands = {"mycmd": self.my_command}

    def my_command(self, args):
        return "Custom command executed!"

def register_plugin():
    return MyPlugin()
```

## 🧪 Testing

Run the test suite to verify everything works:

```bash
# Basic functionality tests
python test_uwu.py

# Enhanced features tests
python test_cmd_enhancements.py

# Run all tests
python -m pytest
```

## 📁 Project Structure

```
UwU-CLI/
├── uwu_cli.py              # Main CLI application
├── utils/                   # Core utility modules
│   ├── ai.py               # AI integration
│   ├── ascii_ui.py         # UI effects and themes
│   ├── cmd_enhancements.py # CMD command enhancements
│   ├── config.py           # Configuration management
│   ├── tokenizer.py        # Context detection
│   └── tts.py              # Text-to-speech
├── plugins/                 # Plugin system
│   └── git_enhancer.py     # Git enhancement plugin
├── phrases/                 # Roast and clapback content
├── scripts/                 # Utility scripts
├── config/                  # Configuration files
├── tts/                     # TTS resources
├── installer.bat            # Windows installer
├── installer.sh             # Linux/macOS installer
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🎯 Roadmap

### Phase 1: Core CMD Replacement ✅

- [x] Basic CMD command execution
- [x] Command aliases and enhancements
- [x] Autosuggestions and tab completion
- [x] Command history management

### Phase 2: Enhanced AI Integration ✅

- [x] OpenRouter API integration
- [x] Multiple AI command types
- [x] Background job processing
- [x] Context-aware responses

### Phase 3: Advanced Features 🚧

- [x] Plugin system architecture
- [x] Colorful themes and effects
- [x] ASCII UI animations
- [ ] Enhanced autosuggestions
- [ ] Oh-My-Zsh style prompts

### Phase 4: Productivity Features 📋

- [ ] Command chaining & piping
- [ ] Smart aliases & functions
- [ ] Integrated development tools
- [ ] Project context detection

### Phase 5: Advanced UI & UX 📋

- [ ] Interactive mode
- [ ] Customizable hotkeys
- [ ] Rich output formatting
- [ ] Performance monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone and setup development environment
git clone https://github.com/ThunderConstellations/UwU-Cli.git
cd UwU-Cli
pip install -r requirements.txt
pip install -e .

# Run tests
python -m pytest

# Format code
black .
flake8 .
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenRouter** - For providing free AI model access
- **DeepSeek** - For the powerful R1 0528 model
- **Community** - For inspiration and feedback
- **UwU Culture** - For the chaotic energy that drives this project

## 🆘 Troubleshooting

### Common Issues

**AI not working?**

- Check your `.env` file has the correct API key
- Verify OpenRouter API key is valid
- Check internet connection

**Commands not found?**

- Ensure you're in the correct directory
- Check if the command is available in your PATH
- Try running `help` to see available commands

**Theme not working?**

- Ensure your terminal supports ANSI colors
- Try a different theme with `theme <name>`
- Check if colorama is properly installed

**Plugin errors?**

- Verify plugin files are in the `plugins/` directory
- Check plugin syntax and imports
- Restart UwU-CLI after adding plugins

### Getting Help

- Check the [Issues](https://github.com/ThunderConstellations/UwU-Cli/issues) page
- Create a new issue with detailed error information
- Join our community discussions

---

**Stay toxic -xoxo LiMcCunt out** 💀✨
