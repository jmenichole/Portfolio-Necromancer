"""
Portfolio Necromancer - Integration tests
Copyright (c) 2025 Portfolio Necromancer Team
Licensed under MIT License - see LICENSE file for details
"""

import pytest
import tempfile
import os
from portfolio_necromancer import PortfolioNecromancer
from portfolio_necromancer.models import Project, Portfolio, ProjectCategory, ProjectSource
from portfolio_necromancer.generator import PortfolioGenerator
from portfolio_necromancer.categorizer import ProjectCategorizer


class TestIntegration:
    """Integration tests for Portfolio Necromancer."""
    
    def test_portfolio_generation_end_to_end(self):
        """Test complete portfolio generation workflow."""
        # Create test projects
        projects = [
            Project(
                title="Test Web App",
                description="A Python web application",
                category=ProjectCategory.CODE,
                source=ProjectSource.MANUAL,
                tags=["python", "flask", "web"]
            ),
            Project(
                title="UI Design",
                description="Modern UI mockup",
                category=ProjectCategory.DESIGN,
                source=ProjectSource.MANUAL,
                tags=["figma", "ui", "design"]
            ),
        ]
        
        # Create portfolio
        portfolio = Portfolio(
            owner_name="Test User",
            owner_email="test@example.com",
            owner_title="Developer",
            owner_bio="Test bio",
            projects=projects
        )
        
        # Generate portfolio in temp directory
        with tempfile.TemporaryDirectory() as tmpdir:
            config = {'output_dir': tmpdir}
            generator = PortfolioGenerator(config)
            output_path = generator.generate(portfolio, 'test_portfolio')
            
            # Verify output files exist
            assert os.path.exists(output_path)
            assert os.path.exists(os.path.join(output_path, 'index.html'))
            assert os.path.exists(os.path.join(output_path, 'assets'))
    
    def test_categorizer_caching(self):
        """Test that categorizer caches results."""
        config = {'api_key': ''}  # No AI, use rule-based
        categorizer = ProjectCategorizer(config)
        
        # Create identical projects
        project1 = Project(
            title="Python Script",
            description="A Python automation script",
            category=ProjectCategory.MISCELLANEOUS,
            source=ProjectSource.MANUAL,
            tags=["python", "automation"],
            confidence_score=0.3  # Low confidence to trigger categorization
        )
        
        project2 = Project(
            title="Python Script",
            description="A Python automation script",
            category=ProjectCategory.MISCELLANEOUS,
            source=ProjectSource.MANUAL,
            tags=["python", "automation"],
            confidence_score=0.3
        )
        
        # Categorize first project (should miss cache)
        category1 = categorizer.categorize(project1)
        
        # Categorize identical project (should hit cache)
        category2 = categorizer.categorize(project2)
        
        # Both should return same category
        assert category1 == category2
        assert category1 == ProjectCategory.CODE
        
        # Check cache was used
        cache_key = categorizer._get_cache_key(project2)
        assert cache_key in categorizer._cache
    
    def test_categorizer_batch_processing(self):
        """Test batch categorization."""
        config = {'api_key': ''}
        categorizer = ProjectCategorizer(config)
        
        projects = [
            Project(
                title="Blog Post",
                description="Article about Python",
                category=ProjectCategory.MISCELLANEOUS,
                source=ProjectSource.MANUAL,
                tags=["writing", "blog"],
                confidence_score=0.3
            ),
            Project(
                title="Logo Design",
                description="Brand identity design",
                category=ProjectCategory.MISCELLANEOUS,
                source=ProjectSource.MANUAL,
                tags=["design", "branding"],
                confidence_score=0.3
            ),
        ]
        
        # Categorize batch
        categorized = categorizer.categorize_batch(projects)
        
        assert len(categorized) == 2
        assert categorized[0].category == ProjectCategory.WRITING
        assert categorized[1].category == ProjectCategory.DESIGN
        # Confidence should be increased
        assert all(p.confidence_score > 0.3 for p in categorized)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
