"""Test categorizer module."""

import pytest
from portfolio_necromancer.models import Project, ProjectCategory, ProjectSource
from portfolio_necromancer.categorizer import ProjectCategorizer


def test_rule_based_categorization():
    """Test rule-based categorization."""
    categorizer = ProjectCategorizer({'api_key': ''})
    
    # Test code project
    code_project = Project(
        title="Python API Development",
        description="Built a REST API using Python and FastAPI",
        category=ProjectCategory.MISCELLANEOUS,
        source=ProjectSource.MANUAL,
        tags=["python", "api"],
        confidence_score=0.3
    )
    
    category = categorizer.categorize(code_project)
    assert category == ProjectCategory.CODE
    
    # Test design project
    design_project = Project(
        title="UI Mockups",
        description="Created beautiful user interface mockups in Figma",
        category=ProjectCategory.MISCELLANEOUS,
        source=ProjectSource.MANUAL,
        tags=["design", "ui"],
        confidence_score=0.3
    )
    
    category = categorizer.categorize(design_project)
    assert category == ProjectCategory.DESIGN
    
    # Test writing project
    writing_project = Project(
        title="Technical Article",
        description="Wrote a comprehensive guide on web development",
        category=ProjectCategory.MISCELLANEOUS,
        source=ProjectSource.MANUAL,
        tags=["writing", "article"],
        confidence_score=0.3
    )
    
    category = categorizer.categorize(writing_project)
    assert category == ProjectCategory.WRITING


def test_high_confidence_skip():
    """Test that high confidence projects are not re-categorized."""
    categorizer = ProjectCategorizer({'api_key': ''})
    
    project = Project(
        title="Test Project",
        description="Test",
        category=ProjectCategory.DESIGN,
        source=ProjectSource.MANUAL,
        confidence_score=0.9  # High confidence
    )
    
    # Even though there are no design keywords, should keep original category
    category = categorizer.categorize(project)
    assert category == ProjectCategory.DESIGN


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
