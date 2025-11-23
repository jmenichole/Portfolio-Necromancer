"""
Portfolio Necromancer - Custom Exception Classes
Copyright (c) 2025 Portfolio Necromancer Team
Licensed under MIT License - see LICENSE file for details
"""


class PortfolioNecromancerError(Exception):
    """Base exception for Portfolio Necromancer."""
    pass


class ConfigurationError(PortfolioNecromancerError):
    """Raised when there's a configuration issue."""
    pass


class ScraperError(PortfolioNecromancerError):
    """Raised when a scraper fails."""
    pass


class AuthenticationError(ScraperError):
    """Raised when authentication fails for a scraper."""
    pass


class CategorizationError(PortfolioNecromancerError):
    """Raised when project categorization fails."""
    pass


class GenerationError(PortfolioNecromancerError):
    """Raised when portfolio generation fails."""
    pass


class ValidationError(PortfolioNecromancerError):
    """Raised when data validation fails."""
    pass
