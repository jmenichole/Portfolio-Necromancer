"""
Portfolio Necromancer - Package setup configuration
Copyright (c) 2025 Portfolio Necromancer Team
Licensed under MIT License - see LICENSE file for details
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="portfolio-necromancer",
    version="0.1.0",
    author="Portfolio Necromancer Team",
    description="Auto-build portfolio sites from your digital work scattered across various platforms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
        "beautifulsoup4>=4.12.0",
        "Pillow>=10.0.0",
        "google-auth>=2.23.0",
        "google-auth-oauthlib>=1.1.0",
        "google-auth-httplib2>=0.1.1",
        "google-api-python-client>=2.100.0",
        "slack-sdk>=3.23.0",
        "openai>=1.3.0",
        "flask>=3.0.0",
        "flask-cors>=4.0.0",
        "jinja2>=3.1.2",
        "pyyaml>=6.0.1",
    ],
    entry_points={
        "console_scripts": [
            "portfolio-necromancer=portfolio_necromancer.cli:main",
        ],
    },
)
