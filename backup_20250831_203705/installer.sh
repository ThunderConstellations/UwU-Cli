#!/bin/bash
# UwU-CLI Complete Installer
# Usage: bash installer.sh

set -e

echo "╔════════════════════════════════════════════╗"
echo "║      ✨ UwU-CLI Complete Installer ✨        ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Python $PYTHON_VERSION detected"

# Check if we're on Windows
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    echo "🪟 Windows environment detected"
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
$PIP_CMD install -r requirements.txt

# Create installation directory
INSTALL_DIR="$HOME/.uwu-cli"
echo ""
echo "📁 Creating installation directory: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

# Copy files
echo "📋 Copying UwU-CLI files..."
cp -r * "$INSTALL_DIR/"

# Make main script executable
chmod +x "$INSTALL_DIR/uwu_cli.py"

# Create launcher script
echo "🔗 Creating launcher script..."
cat > "$INSTALL_DIR/uwu" << 'EOF'
#!/bin/bash
python3 "$HOME/.uwu-cli/uwu_cli.py" "$@"
EOF

chmod +x "$INSTALL_DIR/uwu"

# Add to PATH
echo "🛤️  Adding to PATH..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    SHELL_RC="$HOME/.bashrc"
    if [[ -f "$HOME/.bash_profile" ]]; then
        SHELL_RC="$HOME/.bash_profile"
    fi
else
    # Unix-like
    if [[ -f "$HOME/.bashrc" ]]; then
        SHELL_RC="$HOME/.bashrc"
    elif [[ -f "$HOME/.zshrc" ]]; then
        SHELL_RC="$HOME/.zshrc"
    else
        SHELL_RC="$HOME/.profile"
    fi
fi

# Check if already in PATH
if ! grep -q "uwu-cli" "$SHELL_RC" 2>/dev/null; then
    echo "" >> "$SHELL_RC"
    echo "# UwU-CLI" >> "$SHELL_RC"
    echo 'export PATH="$HOME/.uwu-cli:$PATH"' >> "$SHELL_RC"
    echo "✅ Added to $SHELL_RC"
else
    echo "✅ Already in PATH"
fi

# Create configuration
echo "⚙️  Creating default configuration..."
mkdir -p "$INSTALL_DIR/config"
cat > "$INSTALL_DIR/config/default_config.json" << 'EOF'
{
  "prompt_style": "uwu",
  "enable_telemetry": false,
  "phrase_pack": "default",
  "auto_save_every": 10,
  "max_history": 500,
  "safe_mode": false,
  "theme_colors": true,
  "ascii_effects": true,
  "sound_enabled": false,
  "plugins_enabled": true,
  "ai_enabled": true,
  "default_ai_model": "gpt-4o-mini"
}
EOF

# Create AI configuration
echo "🤖 Creating AI configuration..."
cat > "$INSTALL_DIR/ai_config.json" << 'EOF'
{
  "openrouter_api_key": "",
  "use_local_llm": false,
  "local_llm_cmd": "",
  "model": "gpt-4o-mini",
  "timeout_seconds": 30,
  "max_tokens": 300,
  "temperature": 0.9
}
EOF

echo ""
echo "🎉 UwU-CLI installation complete!"
echo ""
echo "🚀 To start UwU-CLI, run:"
echo "   uwu"
echo ""
echo "📁 Installation directory: $INSTALL_DIR"
echo "⚙️  Configuration: $INSTALL_DIR/config/"
echo "🔌 Plugins: $INSTALL_DIR/plugins/"
echo ""
echo "💡 For AI features, set your OpenRouter API key:"
echo "   export 
echo ""
echo "🔄 Restart your terminal or run: source $SHELL_RC"
echo ""
echo "UwU~ Stay chaotic, stay sparkly! ✨" 