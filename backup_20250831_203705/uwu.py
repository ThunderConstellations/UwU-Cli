#!/usr/bin/env python3
"""
UwU-Cli Launcher Script
This script launches the UwU-Cli shell
"""

import os
import sys
import subprocess

def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the script directory
    os.chdir(script_dir)
    
    # Launch UwU-Cli
    try:
        subprocess.run([sys.executable, "uwu_cli.py"] + sys.argv[1:])
    except KeyboardInterrupt:
        print("\n👋 UwU-Cli terminated. Stay toxic! -xoxo LiMcCunt out")
    except Exception as e:
        print(f"❌ Error launching UwU-Cli: {e}")

if __name__ == "__main__":
    main() 