"""
Portfolio Necromancer - Email/Gmail scraper
Copyright (c) 2025 Portfolio Necromancer Team
Licensed under MIT License - see LICENSE file for details
"""

import os
import re
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from .base import BaseScraper
from ..models import Project, ProjectSource, ProjectCategory


class EmailScraper(BaseScraper):
    """Scraper for email attachments and content."""
    
    def __init__(self, config: Dict[str, Any], google_config: Dict[str, Any]):
        """Initialize email scraper.
        
        Args:
            config: Email scraper configuration
            google_config: Google API configuration
        """
        super().__init__(config)
        self.google_config = google_config
        self.max_messages = config.get('max_messages', 100)
        self.date_range_days = config.get('date_range_days', 365)
        self.service = None
    
    def is_configured(self) -> bool:
        """Check if Gmail API is configured."""
        credentials_file = self.google_config.get('credentials_file', '')
        return os.path.exists(credentials_file) if credentials_file else False
    
    def _authenticate(self):
        """Authenticate with Gmail API."""
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build
            
            SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
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
            
            self.service = build('gmail', 'v1', credentials=creds)
            
        except Exception as e:
            print(f"Failed to authenticate with Gmail: {e}")
            self.service = None
    
    def scrape(self) -> List[Project]:
        """Scrape emails for project-related content.
        
        Returns:
            List of Project objects extracted from emails
        """
        if not self.can_scrape():
            print("Email scraper not configured or disabled")
            return []
        
        self._authenticate()
        if not self.service:
            return []
        
        projects = []
        
        try:
            # Search for emails with attachments or project-related keywords
            date_threshold = datetime.now() - timedelta(days=self.date_range_days)
            query = f'after:{date_threshold.strftime("%Y/%m/%d")} (has:attachment OR subject:(project OR portfolio OR work OR design OR code OR article))'
            
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=self.max_messages
            ).execute()
            
            messages = results.get('messages', [])
            
            for msg in messages[:self.max_messages]:
                try:
                    project = self._extract_project_from_message(msg['id'])
                    if project:
                        projects.append(project)
                except Exception as e:
                    print(f"Error processing message {msg['id']}: {e}")
                    continue
        
        except Exception as e:
            print(f"Error scraping emails: {e}")
        
        return projects
    
    def _extract_project_from_message(self, message_id: str) -> Optional[Project]:
        """Extract project information from an email message.
        
        Args:
            message_id: Gmail message ID
        
        Returns:
            Project object or None
        """
        try:
            msg = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            headers = {h['name']: h['value'] for h in msg['payload']['headers']}
            subject = headers.get('Subject', 'Untitled')
            date_str = headers.get('Date', '')
            
            # Parse date
            try:
                from email.utils import parsedate_to_datetime
                date = parsedate_to_datetime(date_str)
            except:
                date = datetime.now()
            
            # Get message body
            snippet = msg.get('snippet', '')
            
            # Check if it looks like a project
            if not self._is_project_related(subject, snippet):
                return None
            
            # Extract attachments
            attachments = []
            if 'parts' in msg['payload']:
                for part in msg['payload']['parts']:
                    if part.get('filename'):
                        attachments.append(part['filename'])
            
            # Create basic project
            description = snippet[:200] + "..." if len(snippet) > 200 else snippet
            
            return Project(
                title=self._clean_subject(subject),
                description=description,
                category=ProjectCategory.MISCELLANEOUS,  # Will be categorized later
                source=ProjectSource.EMAIL,
                date=date,
                tags=['email'],
                raw_data={
                    'message_id': message_id,
                    'subject': subject,
                    'attachments': attachments,
                    'snippet': snippet
                },
                confidence_score=0.6
            )
        
        except Exception as e:
            print(f"Error extracting project from message: {e}")
            return None
    
    def _is_project_related(self, subject: str, content: str) -> bool:
        """Check if email is project-related.
        
        Args:
            subject: Email subject
            content: Email content snippet
        
        Returns:
            True if likely project-related
        """
        keywords = [
            'project', 'portfolio', 'work', 'design', 'code', 'article',
            'website', 'app', 'development', 'completed', 'finished',
            'delivered', 'client', 'freelance', 'proposal', 'mockup',
            'prototype', 'final', 'draft'
        ]
        
        text = (subject + ' ' + content).lower()
        
        return any(keyword in text for keyword in keywords)
    
    def _clean_subject(self, subject: str) -> str:
        """Clean email subject to make a good project title.
        
        Args:
            subject: Email subject
        
        Returns:
            Cleaned title
        """
        # Remove common prefixes
        subject = re.sub(r'^(Re:|Fwd?:|RE:|FWD?:)\s*', '', subject, flags=re.IGNORECASE)
        
        # Limit length
        if len(subject) > 100:
            subject = subject[:97] + '...'
        
        return subject.strip()
