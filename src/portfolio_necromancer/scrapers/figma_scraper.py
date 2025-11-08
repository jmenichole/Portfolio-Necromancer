"""Figma scraper for design projects."""

from typing import List, Dict, Any, Optional
from datetime import datetime
import requests

from .base import BaseScraper
from ..models import Project, ProjectSource, ProjectCategory


class FigmaScraper(BaseScraper):
    """Scraper for Figma design files."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize Figma scraper.
        
        Args:
            config: Figma configuration including access token
        """
        super().__init__(config)
        self.access_token = config.get('access_token', '')
        self.team_id = config.get('team_id', '')
        self.max_projects = config.get('max_projects', 20)
        self.base_url = 'https://api.figma.com/v1'
    
    def is_configured(self) -> bool:
        """Check if Figma API is configured."""
        return bool(self.access_token)
    
    def scrape(self) -> List[Project]:
        """Scrape Figma for design projects.
        
        Returns:
            List of Project objects
        """
        if not self.can_scrape():
            print("Figma scraper not configured or disabled")
            return []
        
        projects = []
        
        try:
            # Get user's projects
            if self.team_id:
                projects.extend(self._scrape_team_projects())
            else:
                # Get user files
                projects.extend(self._scrape_user_files())
        
        except Exception as e:
            print(f"Error scraping Figma: {e}")
        
        return projects
    
    def _scrape_user_files(self) -> List[Project]:
        """Scrape files from user's recent files.
        
        Returns:
            List of projects
        """
        projects = []
        
        try:
            headers = {'X-Figma-Token': self.access_token}
            
            # Get recent files (Figma doesn't have a direct endpoint for this,
            # so we'd need to use team projects or specific file IDs)
            # For now, this is a placeholder that would need specific implementation
            
            print("Note: Figma API requires team_id or specific file keys to list files")
            
        except Exception as e:
            print(f"Error scraping user files: {e}")
        
        return projects
    
    def _scrape_team_projects(self) -> List[Project]:
        """Scrape projects from a Figma team.
        
        Returns:
            List of projects
        """
        projects = []
        
        try:
            headers = {'X-Figma-Token': self.access_token}
            
            # Get team projects
            url = f"{self.base_url}/teams/{self.team_id}/projects"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            team_projects = data.get('projects', [])
            
            for project_data in team_projects[:self.max_projects]:
                try:
                    # Get files in project
                    project_id = project_data['id']
                    files_url = f"{self.base_url}/projects/{project_id}/files"
                    files_response = requests.get(files_url, headers=headers)
                    files_response.raise_for_status()
                    
                    files_data = files_response.json()
                    files = files_data.get('files', [])
                    
                    for file in files:
                        project = self._create_project_from_file(file, project_data)
                        if project:
                            projects.append(project)
                
                except Exception as e:
                    print(f"Error processing Figma project: {e}")
                    continue
        
        except Exception as e:
            print(f"Error scraping team projects: {e}")
        
        return projects
    
    def _create_project_from_file(self, file: Dict[str, Any], 
                                   project_data: Dict[str, Any]) -> Optional[Project]:
        """Create a project from a Figma file.
        
        Args:
            file: Figma file data
            project_data: Parent project data
        
        Returns:
            Project object or None
        """
        try:
            name = file.get('name', 'Untitled Design')
            file_key = file.get('key', '')
            
            # Parse date
            try:
                last_modified = file.get('last_modified', '')
                date = datetime.fromisoformat(last_modified.replace('Z', '+00:00'))
            except:
                date = datetime.now()
            
            # Build description
            description = f"Figma design file from project: {project_data.get('name', 'Unknown')}"
            
            # Build Figma link
            links = [f"https://www.figma.com/file/{file_key}"] if file_key else []
            
            # Get thumbnail
            images = []
            thumbnail = file.get('thumbnail_url')
            if thumbnail:
                images.append(thumbnail)
            
            return Project(
                title=name,
                description=description,
                category=ProjectCategory.DESIGN,  # Figma is always design
                source=ProjectSource.FIGMA,
                date=date,
                links=links,
                images=images,
                tags=['figma', 'design', project_data.get('name', 'project')],
                raw_data={
                    'file_key': file_key,
                    'project_id': project_data.get('id'),
                    'project_name': project_data.get('name')
                },
                confidence_score=0.8  # High confidence for Figma files
            )
        
        except Exception as e:
            print(f"Error creating project from Figma file: {e}")
            return None
