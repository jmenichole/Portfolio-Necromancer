"""
Portfolio Necromancer - AI-powered project categorization
Copyright (c) 2025 Portfolio Necromancer Team
Licensed under MIT License - see LICENSE file for details
"""

import logging
import hashlib
from typing import List, Optional, Dict
from ..models import Project, ProjectCategory

logger = logging.getLogger(__name__)


class ProjectCategorizer:
    """Categorizes projects using AI and rule-based methods."""
    
    def __init__(self, config: dict):
        """Initialize categorizer.
        
        Args:
            config: AI configuration including API key
        """
        self.config = config
        self.api_key = config.get('api_key', '')
        self.model = config.get('model', 'gpt-3.5-turbo')
        self.use_ai = bool(self.api_key)
        
        # Simple in-memory cache for categorization results
        self._cache: Dict[str, ProjectCategory] = {}
    
    def _get_cache_key(self, project: Project) -> str:
        """Generate cache key for a project.
        
        Args:
            project: Project to generate key for
            
        Returns:
            Cache key string
        """
        # Create hash from title, description, and tags
        content = f"{project.title}|{project.description}|{','.join(sorted(project.tags))}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def categorize(self, project: Project) -> ProjectCategory:
        """Categorize a project.
        
        Args:
            project: Project to categorize
        
        Returns:
            Project category
        """
        # If already confidently categorized, keep it
        if project.confidence_score > 0.7:
            return project.category
        
        # Check cache first
        cache_key = self._get_cache_key(project)
        if cache_key in self._cache:
            logger.debug(f"Cache hit for project: {project.title}")
            return self._cache[cache_key]
        
        # Try AI categorization if available
        if self.use_ai:
            category = self._categorize_with_ai(project)
            if category:
                self._cache[cache_key] = category
                return category
        
        # Fall back to rule-based categorization
        category = self._categorize_with_rules(project)
        self._cache[cache_key] = category
        return category
    
    def categorize_batch(self, projects: List[Project]) -> List[Project]:
        """Categorize a list of projects.
        
        Args:
            projects: List of projects to categorize
        
        Returns:
            List of projects with updated categories
        """
        for project in projects:
            project.category = self.categorize(project)
            project.confidence_score = min(project.confidence_score + 0.2, 1.0)
        
        return projects
    
    def _categorize_with_ai(self, project: Project) -> Optional[ProjectCategory]:
        """Categorize using OpenAI API.
        
        Args:
            project: Project to categorize
        
        Returns:
            Category or None if AI categorization fails
        """
        try:
            import openai
            
            openai.api_key = self.api_key
            
            prompt = f"""Categorize this project into one of these categories: Writing, Design, Code, or Miscellaneous Unicorn Work.

Project Title: {project.title}
Description: {project.description}
Source: {project.source}
Tags: {', '.join(project.tags)}

Respond with ONLY the category name, nothing else."""

            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a project categorization expert. Categorize projects accurately."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
                temperature=0.3
            )
            
            result = response.choices[0].message.content.strip()
            
            # Map response to category
            result_lower = result.lower()
            if 'writing' in result_lower:
                return ProjectCategory.WRITING
            elif 'design' in result_lower:
                return ProjectCategory.DESIGN
            elif 'code' in result_lower:
                return ProjectCategory.CODE
            elif 'miscellaneous' in result_lower or 'unicorn' in result_lower:
                return ProjectCategory.MISCELLANEOUS
            
        except Exception as e:
            logger.warning(f"AI categorization failed: {e}")
        
        return None
    
    def _categorize_with_rules(self, project: Project) -> ProjectCategory:
        """Categorize using rule-based logic.
        
        Args:
            project: Project to categorize
        
        Returns:
            Category
        """
        text = (project.title + ' ' + project.description + ' ' + ' '.join(project.tags)).lower()
        
        # Writing keywords
        writing_keywords = [
            'article', 'blog', 'post', 'writing', 'content', 'copy',
            'documentation', 'guide', 'tutorial', 'story', 'book',
            'whitepaper', 'report', 'paper', 'essay', 'document'
        ]
        
        # Design keywords
        design_keywords = [
            'design', 'mockup', 'ui', 'ux', 'interface', 'wireframe',
            'prototype', 'figma', 'sketch', 'graphic', 'logo', 'brand',
            'illustration', 'visual', 'layout', 'style', 'theme',
            'image', 'photo', 'artwork'
        ]
        
        # Code keywords
        code_keywords = [
            'code', 'programming', 'development', 'software', 'app',
            'application', 'website', 'web', 'api', 'backend', 'frontend',
            'script', 'function', 'algorithm', 'database', 'server',
            'github', 'repository', 'commit', 'pull request', 'deploy',
            'python', 'javascript', 'java', 'react', 'node', 'django'
        ]
        
        # Count matches
        writing_score = sum(1 for kw in writing_keywords if kw in text)
        design_score = sum(1 for kw in design_keywords if kw in text)
        code_score = sum(1 for kw in code_keywords if kw in text)
        
        # Determine category based on highest score
        scores = {
            ProjectCategory.WRITING: writing_score,
            ProjectCategory.DESIGN: design_score,
            ProjectCategory.CODE: code_score
        }
        
        max_score = max(scores.values())
        
        # If no clear category, return miscellaneous
        if max_score == 0:
            return ProjectCategory.MISCELLANEOUS
        
        # Return category with highest score
        for category, score in scores.items():
            if score == max_score:
                return category
        
        return ProjectCategory.MISCELLANEOUS
