"""
Portfolio Necromancer - Scraper tests
Copyright (c) 2025 Portfolio Necromancer Team
Licensed under MIT License - see LICENSE file for details
"""

import pytest
import tempfile
import os
from pathlib import Path
from portfolio_necromancer.scrapers.screenshot_scraper import ScreenshotScraper
from portfolio_necromancer.scrapers.base import BaseScraper
from portfolio_necromancer.models import ProjectCategory, ProjectSource


class TestScreenshotScraper:
    """Tests for screenshot scraper."""
    
    def test_scraper_not_configured(self):
        """Test scraper when folder doesn't exist."""
        config = {'enabled': True, 'folder_path': '/nonexistent/path'}
        scraper = ScreenshotScraper(config)
        
        assert not scraper.is_configured()
        assert not scraper.can_scrape()
    
    def test_scraper_disabled(self):
        """Test scraper when disabled in config."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = {'enabled': False, 'folder_path': tmpdir}
            scraper = ScreenshotScraper(config)
            
            assert scraper.is_configured()  # Path exists
            assert not scraper.can_scrape()  # But disabled
    
    def test_scrape_empty_folder(self):
        """Test scraping empty folder."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = {'enabled': True, 'folder_path': tmpdir}
            scraper = ScreenshotScraper(config)
            
            projects = scraper.scrape()
            assert len(projects) == 0
    
    def test_extract_title_from_filename(self):
        """Test title extraction from filenames."""
        config = {'enabled': True, 'folder_path': '.'}
        scraper = ScreenshotScraper(config)
        
        # Test various filename patterns
        # Note: "screenshot" is removed by the extraction logic
        assert scraper._extract_title_from_filename('my_project_screenshot') == 'My Project'
        assert scraper._extract_title_from_filename('Screenshot_2023_12_25_my_app') == 'My App'
        assert scraper._extract_title_from_filename('design-mockup-final') == 'Design Mockup Final'
    
    def test_categorize_by_filename(self):
        """Test categorization based on filename."""
        config = {'enabled': True, 'folder_path': '.'}
        scraper = ScreenshotScraper(config)
        
        # Design keywords
        assert scraper._categorize_by_filename('ui_mockup_design') == ProjectCategory.DESIGN
        assert scraper._categorize_by_filename('figma_prototype') == ProjectCategory.DESIGN
        
        # Code keywords
        assert scraper._categorize_by_filename('vscode_terminal') == ProjectCategory.CODE
        assert scraper._categorize_by_filename('github_commit') == ProjectCategory.CODE
        
        # Writing keywords
        assert scraper._categorize_by_filename('blog_post_draft') == ProjectCategory.WRITING
        
        # Default
        assert scraper._categorize_by_filename('random_image') == ProjectCategory.MISCELLANEOUS


class TestBaseScraper:
    """Tests for base scraper functionality."""
    
    def test_base_scraper_abstract(self):
        """Test that BaseScraper cannot be instantiated directly."""
        # BaseScraper is abstract, so we need a concrete implementation
        class TestScraper(BaseScraper):
            def scrape(self):
                return []
            
            def is_configured(self):
                return True
        
        config = {'enabled': True}
        scraper = TestScraper(config)
        
        assert scraper.enabled
        assert scraper.can_scrape()
        assert scraper.scrape() == []
    
    def test_scraper_can_scrape_logic(self):
        """Test can_scrape combines enabled and configured checks."""
        class TestScraper(BaseScraper):
            def __init__(self, config, configured):
                super().__init__(config)
                self._configured = configured
            
            def scrape(self):
                return []
            
            def is_configured(self):
                return self._configured
        
        # Enabled and configured
        scraper1 = TestScraper({'enabled': True}, configured=True)
        assert scraper1.can_scrape()
        
        # Enabled but not configured
        scraper2 = TestScraper({'enabled': True}, configured=False)
        assert not scraper2.can_scrape()
        
        # Disabled but configured
        scraper3 = TestScraper({'enabled': False}, configured=True)
        assert not scraper3.can_scrape()
        
        # Disabled and not configured
        scraper4 = TestScraper({'enabled': False}, configured=False)
        assert not scraper4.can_scrape()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
