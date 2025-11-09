"""
Portfolio Necromancer - Basic tests
Copyright (c) 2025 Portfolio Necromancer Team
Licensed under MIT License - see LICENSE file for details
"""

import pytest
from datetime import datetime
from portfolio_necromancer.models import (
    Project, Portfolio, ProjectCategory, ProjectSource
)


def test_project_creation():
    """Test creating a project."""
    project = Project(
        title="Test Project",
        description="A test project description",
        category=ProjectCategory.CODE,
        source=ProjectSource.MANUAL,
        tags=["test", "python"]
    )
    
    assert project.title == "Test Project"
    assert project.category == ProjectCategory.CODE
    assert len(project.tags) == 2


def test_portfolio_creation():
    """Test creating a portfolio."""
    portfolio = Portfolio(
        owner_name="Test User",
        owner_email="test@example.com",
        owner_title="Developer",
        owner_bio="Test bio"
    )
    
    assert portfolio.owner_name == "Test User"
    assert len(portfolio.projects) == 0


def test_portfolio_with_projects():
    """Test portfolio with projects."""
    project1 = Project(
        title="Project 1",
        description="First project",
        category=ProjectCategory.CODE,
        source=ProjectSource.MANUAL
    )
    
    project2 = Project(
        title="Project 2",
        description="Second project",
        category=ProjectCategory.DESIGN,
        source=ProjectSource.MANUAL
    )
    
    portfolio = Portfolio(
        owner_name="Test User",
        owner_email="test@example.com",
        owner_title="Developer",
        owner_bio="Test bio",
        projects=[project1, project2]
    )
    
    assert len(portfolio.projects) == 2
    
    # Test filtering by category
    code_projects = portfolio.get_projects_by_category(ProjectCategory.CODE)
    assert len(code_projects) == 1
    assert code_projects[0].title == "Project 1"


def test_portfolio_category_counts():
    """Test category counting."""
    projects = [
        Project(
            title=f"Code Project {i}",
            description="Test",
            category=ProjectCategory.CODE,
            source=ProjectSource.MANUAL
        )
        for i in range(3)
    ] + [
        Project(
            title=f"Design Project {i}",
            description="Test",
            category=ProjectCategory.DESIGN,
            source=ProjectSource.MANUAL
        )
        for i in range(2)
    ]
    
    portfolio = Portfolio(
        owner_name="Test User",
        owner_email="test@example.com",
        owner_title="Developer",
        owner_bio="Test bio",
        projects=projects
    )
    
    counts = portfolio.get_project_count_by_category()
    assert counts["Code"] == 3
    assert counts["Design"] == 2
    assert counts["Writing"] == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
