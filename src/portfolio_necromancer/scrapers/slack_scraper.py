"""
Portfolio Necromancer - Slack scraper
Copyright (c) 2025 Portfolio Necromancer Team
Licensed under MIT License - see LICENSE file for details
"""

import os
from typing import List, Dict, Any, Optional
from datetime import datetime

from .base import BaseScraper
from ..models import Project, ProjectSource, ProjectCategory


class SlackScraper(BaseScraper):
    """Scraper for Slack messages and threads."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize Slack scraper.
        
        Args:
            config: Slack scraper configuration including token and settings
        """
        super().__init__(config)
        self.token = config.get('token', '')
        self.user_id = config.get('user_id', '')
        self.max_messages = config.get('max_messages', 100)
        self.client = None
    
    def is_configured(self) -> bool:
        """Check if Slack API is configured."""
        return bool(self.token)
    
    def _authenticate(self):
        """Initialize Slack client."""
        try:
            from slack_sdk import WebClient
            self.client = WebClient(token=self.token)
            
            # Test authentication
            response = self.client.auth_test()
            if not response['ok']:
                self.client = None
                
        except Exception as e:
            print(f"Failed to authenticate with Slack: {e}")
            self.client = None
    
    def scrape(self) -> List[Project]:
        """Scrape Slack for project-related messages.
        
        Returns:
            List of Project objects
        """
        if not self.can_scrape():
            print("Slack scraper not configured or disabled")
            return []
        
        self._authenticate()
        if not self.client:
            return []
        
        projects = []
        
        try:
            # Search for project-related messages
            query = 'project OR portfolio OR completed OR finished OR launched OR delivered'
            
            result = self.client.search_messages(
                query=query,
                count=self.max_messages,
                sort='timestamp',
                sort_dir='desc'
            )
            
            if result['ok']:
                messages = result.get('messages', {}).get('matches', [])
                
                for msg in messages:
                    try:
                        project = self._extract_project_from_message(msg)
                        if project:
                            projects.append(project)
                    except Exception as e:
                        print(f"Error processing Slack message: {e}")
                        continue
        
        except Exception as e:
            print(f"Error scraping Slack: {e}")
        
        return projects
    
    def _extract_project_from_message(self, message: Dict[str, Any]) -> Optional[Project]:
        """Extract project from Slack message.
        
        Args:
            message: Slack message data
        
        Returns:
            Project object or None
        """
        try:
            text = message.get('text', '')
            username = message.get('username', 'Unknown')
            
            # Parse timestamp
            try:
                ts = float(message.get('ts', 0))
                date = datetime.fromtimestamp(ts)
            except:
                date = datetime.now()
            
            # Extract title from first line or first sentence
            title = self._extract_title(text)
            
            # Check if message is substantial enough
            if len(text) < 20 or not self._is_project_related(text):
                return None
            
            # Extract links
            links = self._extract_links(text)
            
            # Create description
            description = text[:300] + "..." if len(text) > 300 else text
            
            return Project(
                title=title,
                description=description,
                category=ProjectCategory.MISCELLANEOUS,  # Will be categorized later
                source=ProjectSource.SLACK,
                date=date,
                links=links,
                tags=['slack', username],
                raw_data={
                    'channel': message.get('channel', {}).get('name', 'unknown'),
                    'username': username,
                    'permalink': message.get('permalink', '')
                },
                confidence_score=0.5
            )
        
        except Exception as e:
            print(f"Error extracting project from Slack message: {e}")
            return None
    
    def _extract_title(self, text: str) -> str:
        """Extract a title from message text.
        
        Args:
            text: Message text
        
        Returns:
            Extracted title
        """
        # Try to get first line
        lines = text.split('\n')
        first_line = lines[0].strip()
        
        # If first line is too long, get first sentence
        if len(first_line) > 80:
            sentences = first_line.split('.')
            first_line = sentences[0]
        
        # Limit length
        if len(first_line) > 60:
            first_line = first_line[:57] + '...'
        
        return first_line or 'Slack Discussion'
    
    def _extract_links(self, text: str) -> List[str]:
        """Extract URLs from text.
        
        Args:
            text: Message text
        
        Returns:
            List of URLs
        """
        import re
        url_pattern = r'<(https?://[^>]+)>'
        matches = re.findall(url_pattern, text)
        
        # Also find plain URLs
        plain_url_pattern = r'https?://[^\s<>"]+'
        plain_matches = re.findall(plain_url_pattern, text)
        
        return list(set(matches + plain_matches))
    
    def _is_project_related(self, text: str) -> bool:
        """Check if message is project-related.
        
        Args:
            text: Message text
        
        Returns:
            True if likely project-related
        """
        keywords = [
            'project', 'portfolio', 'work', 'completed', 'finished',
            'launched', 'delivered', 'shipped', 'released', 'built',
            'created', 'designed', 'developed', 'implemented'
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in keywords)
