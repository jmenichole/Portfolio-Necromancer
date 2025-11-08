"""Portfolio website generator."""

import os
import shutil
from pathlib import Path
from typing import Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime

from ..models import Portfolio, ProjectCategory


class PortfolioGenerator:
    """Generates static portfolio websites."""
    
    def __init__(self, config: dict):
        """Initialize generator.
        
        Args:
            config: Portfolio configuration
        """
        self.config = config
        self.output_dir = config.get('output_dir', './generated_portfolios')
        self.theme = config.get('theme', 'modern')
        self.color_scheme = config.get('color_scheme', 'blue')
        
        # Set up Jinja2 environment
        template_dir = Path(__file__).parent.parent / 'templates'
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )
    
    def generate(self, portfolio: Portfolio, output_name: Optional[str] = None) -> str:
        """Generate a complete portfolio website.
        
        Args:
            portfolio: Portfolio data
            output_name: Optional custom output directory name
        
        Returns:
            Path to generated portfolio
        """
        # Create output directory
        if output_name:
            output_path = Path(self.output_dir) / output_name
        else:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = Path(self.output_dir) / f"portfolio_{timestamp}"
        
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate pages
        self._generate_index(portfolio, output_path)
        self._generate_category_pages(portfolio, output_path)
        self._generate_project_pages(portfolio, output_path)
        self._copy_assets(output_path)
        
        print(f"✓ Portfolio generated at: {output_path}")
        
        return str(output_path)
    
    def _generate_index(self, portfolio: Portfolio, output_path: Path):
        """Generate index.html page.
        
        Args:
            portfolio: Portfolio data
            output_path: Output directory path
        """
        template = self.env.get_template('index.html')
        
        # Get project counts by category
        category_counts = portfolio.get_project_count_by_category()
        
        # Render template
        html = template.render(
            portfolio=portfolio,
            category_counts=category_counts,
            theme=self.theme,
            color_scheme=self.color_scheme,
            year=datetime.now().year
        )
        
        # Write file
        output_file = output_path / 'index.html'
        output_file.write_text(html, encoding='utf-8')
    
    def _generate_category_pages(self, portfolio: Portfolio, output_path: Path):
        """Generate category pages.
        
        Args:
            portfolio: Portfolio data
            output_path: Output directory path
        """
        template = self.env.get_template('category.html')
        
        for category in ProjectCategory:
            projects = portfolio.get_projects_by_category(category)
            
            if not projects:
                continue
            
            # Render template
            html = template.render(
                portfolio=portfolio,
                category=category,
                projects=projects,
                theme=self.theme,
                color_scheme=self.color_scheme,
                year=datetime.now().year
            )
            
            # Write file
            filename = f"{category.value.lower().replace(' ', '_')}.html"
            output_file = output_path / filename
            output_file.write_text(html, encoding='utf-8')
    
    def _generate_project_pages(self, portfolio: Portfolio, output_path: Path):
        """Generate individual project pages.
        
        Args:
            portfolio: Portfolio data
            output_path: Output directory path
        """
        template = self.env.get_template('project.html')
        
        # Create projects directory
        projects_dir = output_path / 'projects'
        projects_dir.mkdir(exist_ok=True)
        
        for project in portfolio.projects:
            # Render template
            html = template.render(
                portfolio=portfolio,
                project=project,
                theme=self.theme,
                color_scheme=self.color_scheme,
                year=datetime.now().year
            )
            
            # Write file
            filename = f"project_{project.id}.html"
            output_file = projects_dir / filename
            output_file.write_text(html, encoding='utf-8')
    
    def _copy_assets(self, output_path: Path):
        """Copy CSS, JS, and other assets to output directory.
        
        Args:
            output_path: Output directory path
        """
        # Create assets directory
        assets_dir = output_path / 'assets'
        assets_dir.mkdir(exist_ok=True)
        
        # Copy template assets
        template_assets = Path(__file__).parent.parent / 'templates' / 'assets'
        
        if template_assets.exists():
            for item in template_assets.iterdir():
                if item.is_file():
                    shutil.copy2(item, assets_dir / item.name)
                elif item.is_dir():
                    dest_dir = assets_dir / item.name
                    if dest_dir.exists():
                        shutil.rmtree(dest_dir)
                    shutil.copytree(item, dest_dir)
