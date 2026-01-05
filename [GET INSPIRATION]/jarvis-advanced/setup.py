#!/usr/bin/env python3
"""
Jarvis AI Advanced - Setup Configuration
Complete installation script for the best AI CLI
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="jarvis-ai-advanced",
    version="2.0.0",
    author="Jarvis AI Team",
    description="Advanced AI Coding Assistant with Stunning Terminal Animations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/jarvis-ai-advanced",
    packages=find_packages(exclude=["tests", "docs", "scripts"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "click>=8.1.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "rich>=13.7.0",
        "colorama>=0.4.6",
        "prompt-toolkit>=3.0.43",
        "aioredis>=2.0.1",
        "aiofiles>=23.2.1",
        "httpx>=0.25.2",
        "openai>=1.3.0",
        "anthropic>=0.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.7.0",
        ],
        "quantum": [
            "pennylane>=0.33.0",
            "torch>=2.1.0",
        ],
        "all": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "pennylane>=0.33.0",
            "torch>=2.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "jarvis=cli.jarvis_cli:cli",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="ai assistant cli chatgpt claude coding terminal animations",
)
