#!/bin/bash
# UwU-Cli PATH Setup Script for Linux/macOS
# This script adds UwU-Cli to your PATH permanently

echo "🐍 Setting up UwU-Cli in your PATH..."

# Get the current directory (where UwU-Cli is installed)
UWU_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python is not available in PATH"
    echo "Please install Python and add it to PATH first"
    exit 1
fi

# Determine Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python command not found"
    exit 1
fi

echo "✅ Python found: $($PYTHON_CMD --version)"

# Check if UwU-CLI files exist
if [ ! -f "$UWU_DIR/uwu_cli.py" ]; then
    echo "❌ UwU-CLI files not found in current directory"
    echo "Please run this script from the UwU-CLI installation directory"
    exit 1
fi

# Create a global launcher in a system PATH location
GLOBAL_LAUNCHER_DIR="$HOME/.local/bin"
GLOBAL_LAUNCHER_PATH="$GLOBAL_LAUNCHER_DIR/uwu-cli"

# Ensure the directory exists
mkdir -p "$GLOBAL_LAUNCHER_DIR"

# Create the global launcher script
cat > "$GLOBAL_LAUNCHER_PATH" << EOF
#!/bin/bash
# UwU-CLI Global Launcher
cd "$UWU_DIR"
$PYTHON_CMD uwu_cli.py "\$@"
EOF

# Make the launcher executable
chmod +x "$GLOBAL_LAUNCHER_PATH"

# Add the directory to user PATH
if [[ ":$PATH:" != *":$GLOBAL_LAUNCHER_DIR:"* ]]; then
    # Add to .bashrc if it exists
    if [ -f "$HOME/.bashrc" ]; then
        echo "" >> "$HOME/.bashrc"
        echo "# UwU-CLI PATH" >> "$HOME/.bashrc"
        echo "export PATH=\"\$PATH:$GLOBAL_LAUNCHER_DIR\"" >> "$HOME/.bashrc"
    fi
    
    # Add to .zshrc if it exists
    if [ -f "$HOME/.zshrc" ]; then
        echo "" >> "$HOME/.zshrc"
        echo "# UwU-CLI PATH" >> "$HOME/.zshrc"
        echo "export PATH=\"\$PATH:$GLOBAL_LAUNCHER_DIR\"" >> "$HOME/.zshrc"
    fi
    
    # Add to .profile if it exists
    if [ -f "$HOME/.profile" ]; then
        echo "" >> "$HOME/.profile"
        echo "# UwU-CLI PATH" >> "$HOME/.profile"
        echo "export PATH=\"\$PATH:$GLOBAL_LAUNCHER_DIR\"" >> "$HOME/.profile"
    fi
    
    echo "✅ UwU-Cli added to PATH: $GLOBAL_LAUNCHER_DIR"
else
    echo "ℹ️  UwU-Cli is already in your PATH"
fi

echo ""
echo "✅ Global launcher created: $GLOBAL_LAUNCHER_PATH"
echo "🔄 Please restart your terminal or run 'source ~/.bashrc' for changes to take effect"
echo "🚀 Then you can run 'uwu-cli' from anywhere!"
echo ""
echo "💡 Alternative commands:"
echo "   • uwu-cli (global command)"
echo "   • $PYTHON_CMD uwu_cli.py (from project directory)"
echo "   • ./uwu_cli.py (from project directory)"
echo ""
echo "📝 Note: If you're using a different shell, you may need to add the PATH manually:"
echo "   export PATH=\"\$PATH:$GLOBAL_LAUNCHER_DIR\""
echo "" 