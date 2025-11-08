"""Screenshot analyzer for extracting projects from image files."""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from .base import BaseScraper
from ..models import Project, ProjectSource, ProjectCategory


class ScreenshotScraper(BaseScraper):
    """Scraper for screenshot files."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize screenshot scraper.
        
        Args:
            config: Screenshot scraper configuration
        """
        super().__init__(config)
        self.folder_path = config.get('folder_path', './screenshots')
        self.supported_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
    
    def is_configured(self) -> bool:
        """Check if screenshot folder exists."""
        return os.path.exists(self.folder_path)
    
    def scrape(self) -> List[Project]:
        """Scrape screenshots folder for project images.
        
        Returns:
            List of Project objects
        """
        if not self.can_scrape():
            print(f"Screenshots folder not found: {self.folder_path}")
            return []
        
        projects = []
        
        try:
            folder = Path(self.folder_path)
            
            # Find all image files
            for file_path in folder.rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in self.supported_extensions:
                    try:
                        project = self._create_project_from_screenshot(file_path)
                        if project:
                            projects.append(project)
                    except Exception as e:
                        print(f"Error processing screenshot {file_path}: {e}")
                        continue
        
        except Exception as e:
            print(f"Error scraping screenshots: {e}")
        
        return projects
    
    def _create_project_from_screenshot(self, file_path: Path) -> Optional[Project]:
        """Create a project from a screenshot file.
        
        Args:
            file_path: Path to screenshot file
        
        Returns:
            Project object or None
        """
        try:
            # Get file stats
            stats = file_path.stat()
            modified_time = datetime.fromtimestamp(stats.st_mtime)
            
            # Get file name without extension
            name = file_path.stem
            
            # Try to extract meaningful title from filename
            title = self._extract_title_from_filename(name)
            
            # Get image dimensions if possible
            dimensions = self._get_image_dimensions(file_path)
            
            # Build description
            description = f"Screenshot captured from {file_path.parent.name}"
            if dimensions:
                description += f" ({dimensions[0]}x{dimensions[1]})"
            
            # Categorize based on filename
            category = self._categorize_by_filename(name)
            
            # Get relative path for image reference
            rel_path = str(file_path.absolute())
            
            return Project(
                title=title,
                description=description,
                category=category,
                source=ProjectSource.SCREENSHOT,
                date=modified_time,
                images=[rel_path],
                tags=['screenshot', file_path.suffix[1:]],
                raw_data={
                    'file_path': str(file_path),
                    'file_size': stats.st_size,
                    'dimensions': dimensions
                },
                confidence_score=0.4  # Lower confidence for screenshots
            )
        
        except Exception as e:
            print(f"Error creating project from screenshot: {e}")
            return None
    
    def _extract_title_from_filename(self, filename: str) -> str:
        """Extract a human-readable title from filename.
        
        Args:
            filename: File name without extension
        
        Returns:
            Cleaned title
        """
        # Replace common separators with spaces
        title = filename.replace('_', ' ').replace('-', ' ')
        
        # Remove common screenshot patterns
        import re
        title = re.sub(r'Screenshot[\s_-]*\d{4}[\s_-]*\d{2}[\s_-]*\d{2}', '', title, flags=re.IGNORECASE)
        title = re.sub(r'Screen[\s_]?Shot', '', title, flags=re.IGNORECASE)
        title = re.sub(r'\d{8}[\s_-]*\d{6}', '', title)  # Remove timestamps
        
        # Clean up extra spaces
        title = ' '.join(title.split())
        
        # Capitalize words
        title = title.title()
        
        # Limit length
        if len(title) > 60:
            title = title[:57] + '...'
        
        return title if title else 'Screenshot Project'
    
    def _get_image_dimensions(self, file_path: Path) -> Optional[tuple]:
        """Get image dimensions.
        
        Args:
            file_path: Path to image file
        
        Returns:
            Tuple of (width, height) or None
        """
        try:
            from PIL import Image
            with Image.open(file_path) as img:
                return img.size
        except Exception:
            return None
    
    def _categorize_by_filename(self, filename: str) -> ProjectCategory:
        """Categorize based on filename keywords.
        
        Args:
            filename: File name
        
        Returns:
            Project category
        """
        filename_lower = filename.lower()
        
        # Check for design keywords
        design_keywords = ['design', 'mockup', 'ui', 'ux', 'interface', 'wireframe', 'prototype']
        if any(kw in filename_lower for kw in design_keywords):
            return ProjectCategory.DESIGN
        
        # Check for code keywords
        code_keywords = ['code', 'terminal', 'editor', 'ide', 'vscode', 'github', 'commit']
        if any(kw in filename_lower for kw in code_keywords):
            return ProjectCategory.CODE
        
        # Check for writing keywords
        writing_keywords = ['article', 'blog', 'post', 'document', 'text', 'writing']
        if any(kw in filename_lower for kw in writing_keywords):
            return ProjectCategory.WRITING
        
        return ProjectCategory.MISCELLANEOUS
