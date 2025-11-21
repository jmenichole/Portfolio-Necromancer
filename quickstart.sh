#!/bin/bash

# Portfolio Necromancer Quick Start Script
# This script sets up and runs the Portfolio Necromancer fullstack application

set -e

echo "🧟 Portfolio Necromancer - Quick Start"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Install dependencies
echo ""
echo -e "${BLUE}Installing dependencies...${NC}"
if [ ! -f requirements.txt ]; then
    echo -e "${RED}Error: requirements.txt not found${NC}"
    exit 1
fi
pip install -q --upgrade -r requirements.txt -e .

echo -e "${GREEN}✓ Dependencies installed${NC}"

# Run tests
echo ""
echo -e "${BLUE}Running tests...${NC}"
if [ ! -d tests ]; then
    echo -e "${RED}Warning: tests directory not found, skipping tests${NC}"
else
    python -m pytest tests/ -q
    echo -e "${GREEN}✓ All tests passed${NC}"
fi

# Generate demo portfolio
echo ""
echo -e "${BLUE}Generating demo portfolio...${NC}"
python demo.py

echo -e "${GREEN}✓ Demo portfolio generated${NC}"
echo "  📁 Location: demo_portfolio/demo/"
echo "  🌐 Open demo_portfolio/demo/index.html in your browser"

# Ask if user wants to start the server
echo ""
read -p "Do you want to start the API server now? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${GREEN}🚀 Starting Portfolio Necromancer API Server...${NC}"
    echo ""
    echo "  Dashboard: http://localhost:5000/"
    echo "  API Health: http://localhost:5000/api/health"
    echo ""
    echo "  Press Ctrl+C to stop the server"
    echo ""
    
    python -m portfolio_necromancer.api.server
else
    echo ""
    echo -e "${BLUE}To start the server later, run:${NC}"
    echo "  python -m portfolio_necromancer.api.server"
    echo ""
fi

echo ""
echo -e "${GREEN}Setup complete! 🎉${NC}"
