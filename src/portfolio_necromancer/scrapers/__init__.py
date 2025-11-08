"""Scrapers package."""

from .base import BaseScraper
from .email_scraper import EmailScraper
from .drive_scraper import GoogleDriveScraper
from .slack_scraper import SlackScraper
from .figma_scraper import FigmaScraper
from .screenshot_scraper import ScreenshotScraper

__all__ = [
    'BaseScraper',
    'EmailScraper',
    'GoogleDriveScraper',
    'SlackScraper',
    'FigmaScraper',
    'ScreenshotScraper'
]
