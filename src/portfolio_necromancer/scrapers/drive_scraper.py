"""
Portfolio Necromancer - Google Drive scraper
Copyright (c) 2025 Portfolio Necromancer Team
Licensed under MIT License - see LICENSE file for details
"""

import os
from typing import List, Dict, Any, Optional
from datetime import datetime

from .base import BaseScraper
from ..models import Project, ProjectSource, ProjectCategory


class GoogleDriveScraper(BaseScraper):
    """Scraper for Google Drive files."""
    
    def __init__(self, config: Dict[str, Any], google_config: Dict[str, Any]):
        """Initialize Google Drive scraper.
        
        Args:
            config: Drive scraper configuration
            google_config: Google API configuration
        """
        super().__init__(config)
        self.google_config = google_config
        self.max_files = config.get('max_files', 50)
        self.service = None
    
    def is_configured(self) -> bool:
        """Check if Google Drive API is configured."""
        credentials_file = self.google_config.get('credentials_file', '')
        return os.path.exists(credentials_file) if credentials_file else False
    
    def _authenticate(self):
        """Authenticate with Google Drive API."""
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build
            
            SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
            creds = None
            
            token_file = self.google_config.get('token_file', 'token.json')
            credentials_file = self.google_config.get('credentials_file', 'credentials.json')
            
            if os.path.exists(token_file):
                creds = Credentials.from_authorized_user_file(token_file, SCOPES)
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        credentials_file, SCOPES)
                    creds = flow.run_local_server(port=0)
                
                with open(token_file, 'w') as token:
                    token.write(creds.to_json())
            
            self.service = build('drive', 'v3', credentials=creds)
            
        except Exception as e:
            print(f"Failed to authenticate with Google Drive: {e}")
            self.service = None
    
    def scrape(self) -> List[Project]:
        """Scrape Google Drive for project files.
        
        Returns:
            List of Project objects
        """
        if not self.can_scrape():
            print("Google Drive scraper not configured or disabled")
            return []
        
        self._authenticate()
        if not self.service:
            return []
        
        projects = []
        
        try:
            # Search for relevant files
            query = "(mimeType='application/pdf' or mimeType='application/vnd.google-apps.document' or " \
                   "mimeType='application/vnd.google-apps.presentation' or " \
                   "mimeType contains 'image/' or name contains 'project' or name contains 'portfolio')"
            
            results = self.service.files().list(
                q=query,
                pageSize=self.max_files,
                fields="files(id, name, mimeType, createdTime, modifiedTime, webViewLink, thumbnailLink, description)",
                orderBy="modifiedTime desc"
            ).execute()
            
            files = results.get('files', [])
            
            for file in files:
                try:
                    project = self._create_project_from_file(file)
                    if project:
                        projects.append(project)
                except Exception as e:
                    print(f"Error processing file {file.get('name')}: {e}")
                    continue
        
        except Exception as e:
            print(f"Error scraping Google Drive: {e}")
        
        return projects
    
    def _create_project_from_file(self, file: Dict[str, Any]) -> Optional[Project]:
        """Create a project from a Drive file.
        
        Args:
            file: Google Drive file metadata
        
        Returns:
            Project object or None
        """
        try:
            name = file.get('name', 'Untitled')
            mime_type = file.get('mimeType', '')
            
            # Parse dates
            try:
                created = datetime.fromisoformat(file.get('createdTime', '').replace('Z', '+00:00'))
            except:
                created = datetime.now()
            
            # Determine initial category based on file type
            category = self._categorize_by_mime_type(mime_type)
            
            # Build description
            description = file.get('description', f"File from Google Drive: {name}")
            if not description or description == name:
                description = f"A {mime_type.split('/')[-1]} file from Google Drive"
            
            # Get links
            links = []
            if file.get('webViewLink'):
                links.append(file['webViewLink'])
            
            # Get thumbnail
            images = []
            if file.get('thumbnailLink'):
                images.append(file['thumbnailLink'])
            
            return Project(
                title=name,
                description=description,
                category=category,
                source=ProjectSource.GOOGLE_DRIVE,
                date=created,
                links=links,
                images=images,
                tags=['google-drive', mime_type.split('/')[-1]],
                raw_data={
                    'file_id': file.get('id'),
                    'mime_type': mime_type,
                    'web_link': file.get('webViewLink')
                },
                confidence_score=0.5
            )
        
        except Exception as e:
            print(f"Error creating project from file: {e}")
            return None
    
    def _categorize_by_mime_type(self, mime_type: str) -> ProjectCategory:
        """Categorize project based on MIME type.
        
        Args:
            mime_type: File MIME type
        
        Returns:
            Project category
        """
        if 'document' in mime_type or 'text' in mime_type or 'pdf' in mime_type:
            return ProjectCategory.WRITING
        elif 'image' in mime_type or 'presentation' in mime_type:
            return ProjectCategory.DESIGN
        elif 'spreadsheet' in mime_type:
            return ProjectCategory.CODE  # Could be data analysis
        else:
            return ProjectCategory.MISCELLANEOUS
