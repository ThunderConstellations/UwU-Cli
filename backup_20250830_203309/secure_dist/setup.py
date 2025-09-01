#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UwU-CLI Setup Script
Professional-grade development shell with AI assistance capabilities
"""

from setuptools import setup, find_packages
import os
from pathlib import Path

# Read the README file for long description
def read_readme():
    readme_path = Path(__file__).parent / "README.md"
    if readme_path.exists():
        with open(readme_path, "r", encoding="utf-8") as fh:
            return fh.read()
    return "Professional-grade development shell with AI assistance capabilities"

# Read requirements
def read_requirements():
    req_path = Path(__file__).parent / "requirements.txt"
    if req_path.exists():
        with open(req_path, "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    # Fallback requirements if file not found
    return [
        "requests>=2.25.0",
        "colorama>=0.4.4",
        "pyreadline3>=3.4.1; sys_platform == 'win32'"
    ]

setup(
    name="uwu-cli",
    version="2.0.0",
    author="UwU-CLI Development Team",
    author_email="",
    description="Professional-grade development shell with AI assistance capabilities",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/UwU-CLI/UwU-Cli",
    packages=find_packages(include=['utils*', 'phrases*', 'plugins*', 'tts*']),
    py_modules=['uwu_cli'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Shells",
        "Topic :: Terminals",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Utilities",
        "Topic :: Desktop Environment",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "uwu-cli=uwu_cli:main",
            "uwu=uwu_cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.md", "*.txt", "*.bat", "*.ps1", "*.sh"],
    },
    keywords="cli shell development ai assistant cursor ide terminal windows powershell bash",
    project_urls={
        "Bug Reports": "https://github.com/UwU-CLI/UwU-Cli/issues",
        "Source": "https://github.com/UwU-CLI/UwU-Cli",
        "Documentation": "https://github.com/UwU-CLI/UwU-Cli#readme",
        "Changelog": "https://github.com/UwU-CLI/UwU-Cli/blob/main/CHANGELOG.md",
    },
    platforms=["Windows", "macOS", "Linux"],
    zip_safe=False,
)
