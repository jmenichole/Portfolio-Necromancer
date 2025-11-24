"""
Portfolio Necromancer - AI-powered project summary generator
Copyright (c) 2025 Portfolio Necromancer Team
Licensed under MIT License - see LICENSE file for details
"""

import logging
from typing import List, Optional
from ..models import Project

logger = logging.getLogger(__name__)


class ProjectSummarizer:
    """Generates AI-powered summaries for projects."""
    
    def __init__(self, config: dict, user_name: str = "The developer"):
        """Initialize summarizer.
        
        Args:
            config: AI configuration including API key
            user_name: User's name for personalized summaries
        """
        self.config = config
        self.api_key = config.get('api_key', '')
        self.model = config.get('model', 'gpt-3.5-turbo')
        self.max_tokens = config.get('max_tokens', 500)
        self.user_name = user_name
        self.use_ai = bool(self.api_key)
    
    def generate_summary(self, project: Project) -> str:
        """Generate a summary for a project.
        
        Args:
            project: Project to summarize
        
        Returns:
            AI-generated summary
        """
        # If project already has a good AI summary, keep it
        if project.ai_summary and len(project.ai_summary) > 50:
            return project.ai_summary
        
        # Try AI summary if available
        if self.use_ai:
            summary = self._generate_with_ai(project)
            if summary:
                return summary
        
        # Fall back to template-based summary
        return self._generate_with_template(project)
    
    def generate_summaries_batch(self, projects: List[Project]) -> List[Project]:
        """Generate summaries for a list of projects.
        
        Args:
            projects: List of projects to summarize
        
        Returns:
            List of projects with AI summaries
        """
        for project in projects:
            project.ai_summary = self.generate_summary(project)
        
        return projects
    
    def _generate_with_ai(self, project: Project) -> Optional[str]:
        """Generate summary using OpenAI API.
        
        Args:
            project: Project to summarize
        
        Returns:
            Summary or None if generation fails
        """
        try:
            import openai
            
            openai.api_key = self.api_key
            
            prompt = f"""Write a professional, impressive portfolio summary for this project. 
Make it sound accomplishment-focused and highlight the value delivered.

Format: "In this project, {self.user_name} skillfully [action verb] [description] to deliver [outcome/impact]."

Project Details:
Title: {project.title}
Category: {project.category}
Description: {project.description}
Source: {project.source}
Tags: {', '.join(project.tags)}

Write ONE compelling paragraph (2-3 sentences) that makes this project sound impressive and impactful."""

            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at writing compelling portfolio descriptions that highlight achievements and impact."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=0.7
            )
            
            summary = response.choices[0].message.content.strip()
            
            # Clean up the summary
            summary = summary.replace('"', '').replace("'", "'")
            
            return summary
            
        except Exception as e:
            logger.warning(f"AI summary generation failed: {e}")
        
        return None
    
    def _generate_with_template(self, project: Project) -> str:
        """Generate summary using templates.
        
        Args:
            project: Project to summarize
        
        Returns:
            Template-based summary
        """
        templates = {
            "Writing": [
                f"In this project, {self.user_name} crafted compelling content that engaged readers and delivered clear value through thoughtful writing.",
                f"In this {project.category.lower()} project, {self.user_name} produced high-quality written content that effectively communicated key ideas and insights.",
            ],
            "Design": [
                f"In this project, {self.user_name} created visually stunning designs that balanced aesthetics with functionality to deliver an exceptional user experience.",
                f"In this {project.category.lower()} project, {self.user_name} designed intuitive interfaces that enhanced usability and visual appeal.",
            ],
            "Code": [
                f"In this project, {self.user_name} developed robust, efficient code that solved complex technical challenges and delivered measurable results.",
                f"In this {project.category.lower()} project, {self.user_name} built scalable software solutions that met technical requirements and exceeded expectations.",
            ],
            "Miscellaneous Unicorn Work": [
                f"In this project, {self.user_name} demonstrated versatility and creativity by delivering exceptional results across multiple disciplines.",
                f"In this unique project, {self.user_name} skillfully combined diverse skills to create something truly remarkable.",
            ]
        }
        
        # Get templates for category
        category_templates = templates.get(project.category, templates["Miscellaneous Unicorn Work"])
        
        # Use hash of project title to consistently pick same template
        template_index = hash(project.title) % len(category_templates)
        
        return category_templates[template_index]
