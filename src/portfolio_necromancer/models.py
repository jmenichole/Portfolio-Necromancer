"""
Portfolio Necromancer - Data models
Copyright (c) 2025 Portfolio Necromancer Team
Licensed under MIT License - see LICENSE file for details
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


class ProjectCategory(str, Enum):
    """Project categories."""
    WRITING = "Writing"
    DESIGN = "Design"
    CODE = "Code"
    MISCELLANEOUS = "Miscellaneous Unicorn Work"


class ProjectSource(str, Enum):
    """Source platforms for projects."""
    EMAIL = "email"
    GOOGLE_DRIVE = "google_drive"
    GOOGLE_DOCS = "google_docs"
    FIGMA = "figma"
    SLACK = "slack"
    SCREENSHOT = "screenshot"
    MANUAL = "manual"


class Project(BaseModel):
    """Represents a single project in the portfolio."""
    
    model_config = {"use_enum_values": True}
    
    id: str = Field(default_factory=lambda: datetime.now().strftime("%Y%m%d%H%M%S"))
    title: str
    description: str
    category: ProjectCategory
    source: ProjectSource
    date: datetime = Field(default_factory=datetime.now)
    tags: List[str] = Field(default_factory=list)
    
    # Optional fields
    images: List[str] = Field(default_factory=list)  # URLs or paths to images
    links: List[str] = Field(default_factory=list)  # External links
    client: Optional[str] = None
    ai_summary: Optional[str] = None
    
    # Metadata
    raw_data: Optional[Dict[str, Any]] = None
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)


class Portfolio(BaseModel):
    """Represents a complete portfolio."""
    
    owner_name: str
    owner_email: str
    owner_title: str
    owner_bio: str
    
    projects: List[Project] = Field(default_factory=list)
    
    # Settings
    theme: str = "modern"
    color_scheme: str = "blue"
    
    # Feature flags
    custom_domain: Optional[str] = None
    custom_branding: bool = False
    show_watermark: bool = True
    
    # Generated metadata
    generated_at: datetime = Field(default_factory=datetime.now)
    
    def get_projects_by_category(self, category: ProjectCategory) -> List[Project]:
        """Get all projects in a specific category."""
        return [p for p in self.projects if p.category == category]
    
    def get_project_count_by_category(self) -> Dict[str, int]:
        """Get count of projects in each category."""
        counts = {cat.value: 0 for cat in ProjectCategory}
        for project in self.projects:
            counts[project.category] += 1
        return counts


class UserConfig(BaseModel):
    """User configuration for Portfolio Necromancer."""
    
    name: str
    email: str
    title: str
    bio: str
    
    # API credentials
    openai_api_key: Optional[str] = None
    google_credentials_path: Optional[str] = None
    slack_token: Optional[str] = None
    figma_token: Optional[str] = None
    
    # Feature flags
    pro_features_enabled: bool = False
    custom_domain: Optional[str] = None
    custom_branding: bool = False
