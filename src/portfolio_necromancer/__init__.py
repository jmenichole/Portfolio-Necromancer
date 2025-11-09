"""
Portfolio Necromancer - Auto-generate portfolios from scattered digital work
Copyright (c) 2025 Portfolio Necromancer Team
Licensed under MIT License - see LICENSE file for details
"""

__version__ = "0.1.0"
__author__ = "Portfolio Necromancer Team"
__description__ = "Auto-build portfolio sites from your digital work scattered across various platforms"

from .models import Project, Portfolio
from .necromancer import PortfolioNecromancer

__all__ = ["PortfolioNecromancer", "Project", "Portfolio"]
