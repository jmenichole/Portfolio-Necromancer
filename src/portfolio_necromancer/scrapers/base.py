"""Base scraper interface."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from ..models import Project


class BaseScraper(ABC):
    """Abstract base class for all scrapers."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize scraper with configuration.
        
        Args:
            config: Configuration dictionary for the scraper
        """
        self.config = config
        self.enabled = config.get('enabled', True)
    
    @abstractmethod
    def scrape(self) -> List[Project]:
        """Scrape data and return list of projects.
        
        Returns:
            List of Project objects
        """
        pass
    
    @abstractmethod
    def is_configured(self) -> bool:
        """Check if scraper is properly configured.
        
        Returns:
            True if configured, False otherwise
        """
        pass
    
    def can_scrape(self) -> bool:
        """Check if scraper can run.
        
        Returns:
            True if scraper is enabled and configured
        """
        return self.enabled and self.is_configured()
