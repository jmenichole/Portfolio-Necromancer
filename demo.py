"""
Portfolio Necromancer - Demo script showing usage with sample data
Copyright (c) 2025 Portfolio Necromancer Team
Licensed under MIT License - see LICENSE file for details
"""

from datetime import datetime, timedelta
import random

from portfolio_necromancer.models import (
    Portfolio, Project, ProjectCategory, ProjectSource
)
from portfolio_necromancer.categorizer import ProjectCategorizer, ProjectSummarizer
from portfolio_necromancer.generator import PortfolioGenerator


def create_demo_projects():
    """Create sample projects for demonstration."""
    projects = [
        Project(
            title="E-Commerce Platform Redesign",
            description="Complete redesign of a major e-commerce platform with focus on UX and conversion optimization.",
            category=ProjectCategory.DESIGN,
            source=ProjectSource.FIGMA,
            date=datetime.now() - timedelta(days=30),
            tags=["ui/ux", "figma", "e-commerce", "web design"],
            images=[],
            client="TechCorp Inc"
        ),
        Project(
            title="RESTful API Development",
            description="Built a scalable REST API using Python and FastAPI for a mobile application backend.",
            category=ProjectCategory.CODE,
            source=ProjectSource.EMAIL,
            date=datetime.now() - timedelta(days=60),
            tags=["python", "fastapi", "rest", "backend", "api"],
            links=["https://github.com/example/api-project"]
        ),
        Project(
            title="Technical Blog Series on Machine Learning",
            description="5-part blog series explaining machine learning concepts to beginners with practical examples.",
            category=ProjectCategory.WRITING,
            source=ProjectSource.GOOGLE_DOCS,
            date=datetime.now() - timedelta(days=45),
            tags=["writing", "machine learning", "tutorial", "blog"],
            links=["https://medium.com/@example/ml-series"]
        ),
        Project(
            title="Mobile App UI Mockups",
            description="Created high-fidelity mockups for a fitness tracking mobile application with dark mode support.",
            category=ProjectCategory.DESIGN,
            source=ProjectSource.FIGMA,
            date=datetime.now() - timedelta(days=15),
            tags=["mobile", "ui", "figma", "fitness", "dark mode"]
        ),
        Project(
            title="Data Analysis Dashboard",
            description="Interactive dashboard for sales data visualization using React and D3.js.",
            category=ProjectCategory.CODE,
            source=ProjectSource.SLACK,
            date=datetime.now() - timedelta(days=90),
            tags=["react", "javascript", "data viz", "d3.js", "dashboard"],
            links=["https://demo.example.com/dashboard"]
        ),
        Project(
            title="Brand Identity Guide",
            description="Complete brand identity documentation including logo usage, color palette, and typography guidelines.",
            category=ProjectCategory.DESIGN,
            source=ProjectSource.GOOGLE_DRIVE,
            date=datetime.now() - timedelta(days=120),
            tags=["branding", "design", "style guide", "identity"]
        ),
        Project(
            title="Product Launch Strategy Document",
            description="Comprehensive go-to-market strategy for a SaaS product including competitor analysis and marketing plan.",
            category=ProjectCategory.WRITING,
            source=ProjectSource.GOOGLE_DOCS,
            date=datetime.now() - timedelta(days=75),
            tags=["strategy", "marketing", "saas", "business"]
        ),
        Project(
            title="Automated Testing Framework",
            description="Developed a comprehensive automated testing framework using Pytest and Selenium for web applications.",
            category=ProjectCategory.CODE,
            source=ProjectSource.EMAIL,
            date=datetime.now() - timedelta(days=100),
            tags=["python", "testing", "selenium", "pytest", "automation"]
        ),
        Project(
            title="Conference Talk: Future of Web Development",
            description="45-minute presentation at WebDev Summit covering emerging trends in web development.",
            category=ProjectCategory.MISCELLANEOUS,
            source=ProjectSource.SCREENSHOT,
            date=datetime.now() - timedelta(days=50),
            tags=["speaking", "web dev", "conference", "presentation"]
        ),
        Project(
            title="Chrome Extension for Productivity",
            description="Built a browser extension to help users track time and manage tasks directly from their browser.",
            category=ProjectCategory.CODE,
            source=ProjectSource.MANUAL,
            date=datetime.now() - timedelta(days=80),
            tags=["javascript", "chrome extension", "productivity", "web"]
        ),
    ]
    
    return projects


def generate_demo_portfolio():
    """Generate a complete demo portfolio."""
    print("🧟 Portfolio Necromancer - Demo Mode")
    print("=" * 60)
    print()
    
    # Create sample projects
    print("📦 Creating sample projects...")
    projects = create_demo_projects()
    print(f"✓ Created {len(projects)} sample projects")
    print()
    
    # Generate AI summaries (using templates since we likely don't have API key in demo)
    print("✨ Generating summaries...")
    summarizer = ProjectSummarizer({'api_key': ''}, "Alex Smith")
    projects = summarizer.generate_summaries_batch(projects)
    print("✓ Summaries generated")
    print()
    
    # Create portfolio
    portfolio = Portfolio(
        owner_name="Alex Smith",
        owner_email="alex.smith@example.com",
        owner_title="Full-Stack Developer & Designer",
        owner_bio="I'm a versatile creator who loves building beautiful, functional products. "
                 "From design to deployment, I bring ideas to life with clean code and thoughtful UX.",
        projects=projects,
        theme="modern",
        color_scheme="blue",
        show_watermark=True
    )
    
    # Generate portfolio website
    print("🎨 Generating portfolio website...")
    generator = PortfolioGenerator({
        'output_dir': './demo_portfolio',
        'theme': 'modern',
        'color_scheme': 'blue'
    })
    
    output_path = generator.generate(portfolio, 'demo')
    print()
    
    # Print summary
    print("=" * 60)
    print("🎉 Demo Portfolio Generated!")
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
    print(f"🌐 Open {output_path}/index.html in your browser to view")
    print()
    print("=" * 60)


if __name__ == '__main__':
    generate_demo_portfolio()
