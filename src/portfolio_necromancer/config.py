"""Configuration management for Portfolio Necromancer."""

import os
import yaml
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv


class Config:
    """Configuration manager."""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration.
        
        Args:
            config_file: Path to YAML config file. If None, looks for config.yaml
        """
        load_dotenv()  # Load environment variables
        
        self.config_file = config_file or self._find_config_file()
        self.config: Dict[str, Any] = {}
        
        if self.config_file and os.path.exists(self.config_file):
            self._load_config()
        else:
            self._load_defaults()
    
    def _find_config_file(self) -> Optional[str]:
        """Find config file in common locations."""
        search_paths = [
            "config.yaml",
            "config.yml",
            os.path.expanduser("~/.portfolio-necromancer/config.yaml"),
        ]
        
        for path in search_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def _load_config(self):
        """Load configuration from YAML file."""
        with open(self.config_file, 'r') as f:
            self.config = yaml.safe_load(f) or {}
    
    def _load_defaults(self):
        """Load default configuration."""
        self.config = {
            'user': {
                'name': os.getenv('USER_NAME', 'Your Name'),
                'email': os.getenv('USER_EMAIL', 'your.email@example.com'),
                'title': os.getenv('USER_TITLE', 'Freelancer'),
                'bio': os.getenv('USER_BIO', 'A passionate creator'),
            },
            'ai': {
                'api_key': os.getenv('OPENAI_API_KEY', ''),
                'model': os.getenv('AI_MODEL', 'gpt-3.5-turbo'),
                'max_tokens': int(os.getenv('AI_MAX_TOKENS', '500')),
            },
            'google': {
                'credentials_file': os.getenv('GOOGLE_CREDENTIALS', 'credentials.json'),
                'token_file': os.getenv('GOOGLE_TOKEN', 'token.json'),
            },
            'slack': {
                'token': os.getenv('SLACK_TOKEN', ''),
                'user_id': os.getenv('SLACK_USER_ID', ''),
            },
            'figma': {
                'access_token': os.getenv('FIGMA_TOKEN', ''),
                'team_id': os.getenv('FIGMA_TEAM_ID', ''),
            },
            'scraping': {
                'email': {'enabled': True, 'max_messages': 100},
                'drive': {'enabled': True, 'max_files': 50},
                'slack': {'enabled': True, 'max_messages': 100},
                'figma': {'enabled': True, 'max_projects': 20},
                'screenshots': {'enabled': True, 'folder_path': './screenshots'},
            },
            'categories': [
                'Writing',
                'Design',
                'Code',
                'Miscellaneous Unicorn Work'
            ],
            'portfolio': {
                'output_dir': './generated_portfolios',
                'theme': 'modern',
                'color_scheme': 'blue',
                'items_per_page': 12,
            },
            'features': {
                'custom_domain': False,
                'custom_branding': False,
                'advanced_analytics': False,
                'unlimited_projects': False,
                'remove_watermark': False,
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key.
        
        Args:
            key: Configuration key in dot notation (e.g., 'user.name')
            default: Default value if key not found
        
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value by dot-notation key.
        
        Args:
            key: Configuration key in dot notation
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self, output_file: Optional[str] = None):
        """Save configuration to file.
        
        Args:
            output_file: Path to save config. If None, uses original file.
        """
        output = output_file or self.config_file or 'config.yaml'
        
        # Create directory if it doesn't exist
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
