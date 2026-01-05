#!/usr/bin/env python3
"""
Setup script for Jarvis AI CLI
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="jarvis-ai-advanced",
    version="2.0.0",
    author="Ashutosh Karn",
    description="Advanced AI Coding Assistant with Beautiful CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/jarvis-ai",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
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
        "openai>=1.3.0",
        "anthropic>=0.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
        "quantum": [
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
)
