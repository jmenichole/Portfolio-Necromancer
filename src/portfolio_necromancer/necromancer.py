"""
Portfolio Necromancer - Main orchestrator
Copyright (c) 2025 Portfolio Necromancer Team
Licensed under MIT License - see LICENSE file for details
"""

import logging
from typing import List, Optional
from .models import Portfolio, Project
from .config import Config
from .scrapers.email_scraper import EmailScraper
from .scrapers.drive_scraper import GoogleDriveScraper
from .scrapers.slack_scraper import SlackScraper
from .scrapers.figma_scraper import FigmaScraper
from .scrapers.screenshot_scraper import ScreenshotScraper
from .categorizer import ProjectCategorizer, ProjectSummarizer
from .generator import PortfolioGenerator

logger = logging.getLogger(__name__)


class PortfolioNecromancer:
    """Main orchestrator for portfolio generation from scattered digital work."""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize Portfolio Necromancer.
        
        Args:
            config_file: Path to configuration file
        """
        self.config = Config(config_file)
        
        # Initialize scrapers
        google_config = {
            'credentials_file': self.config.get('google.credentials_file', ''),
            'token_file': self.config.get('google.token_file', ''),
        }
        
        slack_config = {
            'token': self.config.get('slack.token', ''),
            'user_id': self.config.get('slack.user_id', ''),
            **self.config.get('scraping.slack', {})
        }
        
        figma_config = {
            'access_token': self.config.get('figma.access_token', ''),
            'team_id': self.config.get('figma.team_id', ''),
            **self.config.get('scraping.figma', {})
        }
        
        self.scrapers = [
            EmailScraper(self.config.get('scraping.email', {}), google_config),
            GoogleDriveScraper(self.config.get('scraping.drive', {}), google_config),
            SlackScraper(slack_config),
            FigmaScraper(figma_config),
            ScreenshotScraper(self.config.get('scraping.screenshots', {})),
        ]
        
        # Initialize categorizer and summarizer
        ai_config = self.config.get('ai', {})
        self.categorizer = ProjectCategorizer(ai_config)
        self.summarizer = ProjectSummarizer(ai_config, self.config.get('user.name', 'The developer'))
        
        # Initialize generator
        self.generator = PortfolioGenerator(self.config.get('portfolio', {}))
    
    def resurrect(self, output_name: Optional[str] = None) -> str:
        """Resurrect portfolio from digital wreckage.
        
        This is the main method that:
        1. Scrapes all configured sources
        2. Categorizes projects
        3. Generates AI summaries
        4. Creates portfolio website
        
        Args:
            output_name: Optional custom name for the output portfolio
        
        Returns:
            Path to generated portfolio
        """
        logger.info("🧟 Portfolio Necromancer: Resurrecting your portfolio from digital wreckage...")
        
        # Step 1: Scrape all sources
        logger.info("📥 Scraping data from all sources...")
        projects = self._scrape_all()
        logger.info(f"✓ Found {len(projects)} potential projects")
        
        if not projects:
            logger.error("❌ No projects found. Please check your configuration and data sources.")
            return ""
        
        # Step 2: Categorize projects
        logger.info("🏷️  Categorizing projects...")
        projects = self.categorizer.categorize_batch(projects)
        logger.info("✓ Projects categorized")
        
        # Step 3: Generate AI summaries
        logger.info("✨ Generating AI-powered summaries...")
        projects = self.summarizer.generate_summaries_batch(projects)
        logger.info("✓ Summaries generated")
        
        # Step 4: Create portfolio object
        portfolio = Portfolio(
            owner_name=self.config.get('user.name', 'Your Name'),
            owner_email=self.config.get('user.email', 'your@email.com'),
            owner_title=self.config.get('user.title', 'Freelancer'),
            owner_bio=self.config.get('user.bio', 'A passionate creator'),
            projects=projects,
            theme=self.config.get('portfolio.theme', 'modern'),
            color_scheme=self.config.get('portfolio.color_scheme', 'blue'),
            custom_domain=self.config.get('features.custom_domain'),
            custom_branding=self.config.get('features.custom_branding', False),
            show_watermark=not self.config.get('features.remove_watermark', False),
        )
        
        # Apply free tier limits if not pro
        if not self.config.get('features.unlimited_projects', False):
            portfolio.projects = portfolio.projects[:20]  # Free tier: max 20 projects
        
        # Step 5: Generate portfolio website
        logger.info("🎨 Generating portfolio website...")
        output_path = self.generator.generate(portfolio, output_name)
        
        # Print summary
        self._print_summary(portfolio, output_path)
        
        return output_path
    
    def _scrape_all(self) -> List[Project]:
        """Run all configured scrapers.
        
        Returns:
            Combined list of all scraped projects
        """
        all_projects = []
        
        for scraper in self.scrapers:
            scraper_name = scraper.__class__.__name__
            
            if not scraper.can_scrape():
                logger.debug(f"⊘ {scraper_name}: Skipped (not configured or disabled)")
                continue
            
            logger.info(f"→ {scraper_name}: Scraping...")
            
            try:
                projects = scraper.scrape()
                all_projects.extend(projects)
                logger.info(f"  ✓ Found {len(projects)} projects")
            except Exception as e:
                logger.error(f"  ✗ Error in {scraper_name}: {e}", exc_info=True)
        
        return all_projects
    
    def _print_summary(self, portfolio: Portfolio, output_path: str):
        """Print a summary of the generated portfolio.
        
        Args:
            portfolio: Generated portfolio
            output_path: Path to output directory
        """
        print("=" * 60)
        print("🎉 Portfolio Successfully Resurrected!")
        print("=" * 60)
        print()
        print(f"Owner: {portfolio.owner_name}")
        print(f"Total Projects: {len(portfolio.projects)}")
        print()
        print("Projects by Category:")
        
        category_counts = portfolio.get_project_count_by_category()
        for category, count in category_counts.items():
            if count > 0:
                print(f"  • {category}: {count}")
        
        print()
        print(f"📁 Portfolio Location: {output_path}")
        print(f"🌐 Open index.html in your browser to view")
        print()
        
        # Show feature status
        if not portfolio.custom_branding:
            print("💡 Tip: Upgrade to Pro to remove watermark and add custom branding!")
        
        print("=" * 60)
