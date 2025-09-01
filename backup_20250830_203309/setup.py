#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UwU-CLI Setup Script
Professional-grade development shell with AI assistance capabilities
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="uwu-cli",
    version="2.3.0",
    author="UwU-CLI Development Team",
    author_email="",
    description="Professional-grade development shell with AI assistance capabilities",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/UwU-CLI/UwU-Cli",
    packages=find_packages(include=['utils*']),
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
    # PyPI specific - Generic URLs
    download_url="https://github.com/UwU-CLI/UwU-Cli/archive/refs/tags/v2.0.0.tar.gz",
    platforms=["Windows", "macOS", "Linux"],
    zip_safe=False,
) 