"""
Flask API Application for Portfolio Necromancer
Provides REST API endpoints for portfolio generation and management
"""

import logging
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import tempfile
import shutil
from pydantic import BaseModel, Field, ValidationError as PydanticValidationError

from ..models import Portfolio, Project, ProjectCategory, ProjectSource
from ..necromancer import PortfolioNecromancer
from ..generator import PortfolioGenerator
from ..config import Config
from ..exceptions import ValidationError

logger = logging.getLogger(__name__)


# Pydantic models for API request validation
class OwnerInfo(BaseModel):
    """Owner information for portfolio generation."""
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=3, max_length=100)
    title: str = Field(default="Developer", max_length=100)
    bio: str = Field(default="", max_length=500)


class ProjectRequest(BaseModel):
    """Project information for API requests."""
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    category: str = Field(default="code", max_length=50)
    tags: List[str] = Field(default_factory=list)
    url: Optional[str] = Field(default=None, max_length=500)
    image_url: Optional[str] = Field(default=None, max_length=500)


class GeneratePortfolioRequest(BaseModel):
    """Request model for portfolio generation."""
    owner: OwnerInfo
    projects: List[ProjectRequest] = Field(..., min_length=1, max_length=100)
    theme: str = Field(default="modern", max_length=50)
    color_scheme: str = Field(default="blue", max_length=50)
    show_watermark: bool = Field(default=True)


def create_app(config: Dict[str, Any] = None) -> Flask:
    """Create and configure the Flask application.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured Flask application
    """
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    
    # Enable CORS for all routes
    CORS(app)
    
    def is_dev_or_test_environment() -> bool:
        """Check if running in development or testing mode."""
        return (
            os.environ.get('FLASK_ENV') == 'development' or
            (config and config.get('TESTING'))
        )
    
    # Configuration
    # Security: SECRET_KEY must be set in production via environment variable
    secret_key = os.environ.get('SECRET_KEY')
    if not secret_key:
        # Only allow default in development or testing mode
        if is_dev_or_test_environment():
            secret_key = 'dev-secret-key-for-development-only'
        else:
            raise ValueError("SECRET_KEY environment variable must be set in production")
    
    app.config['SECRET_KEY'] = secret_key
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Storage directory for generated portfolios
    STORAGE_DIR = os.path.join(tempfile.gettempdir(), 'portfolio_necromancer_api')
    os.makedirs(STORAGE_DIR, exist_ok=True)
    
    if config:
        app.config.update(config)
    
    # Static file directory
    STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')
    
    @app.route('/')
    def index():
        """Serve the dashboard."""
        return send_file(os.path.join(STATIC_DIR, 'dashboard.html'))
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'version': '0.1.0',
            'timestamp': datetime.now(timezone.utc).isoformat()
        })
    
    @app.route('/api/generate', methods=['POST'])
    def generate_portfolio():
        """Generate a portfolio from provided data.
        
        Request body:
        {
            "owner": {
                "name": "Your Name",
                "email": "email@example.com",
                "title": "Your Title",
                "bio": "Your bio"
            },
            "projects": [
                {
                    "title": "Project Title",
                    "description": "Project description",
                    "category": "code",
                    "tags": ["python", "web"],
                    "url": "https://project.com"
                }
            ],
            "theme": "modern",
            "color_scheme": "blue"
        }
        
        Returns:
            JSON with portfolio_id and download URL
        """
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            # Validate request with Pydantic
            try:
                request_data = GeneratePortfolioRequest(**data)
            except PydanticValidationError as e:
                logger.warning(f"Validation error: {e}")
                return jsonify({
                    'error': 'Invalid request data',
                    'details': e.errors()
                }), 400
            
            # Convert projects to Project objects
            projects = []
            for proj_data in request_data.projects:
                try:
                    category_str = proj_data.category.upper()
                    category = ProjectCategory[category_str] if category_str in ProjectCategory.__members__ else ProjectCategory.CODE
                    
                    # Fix field name mismatches: url→links, image_url→images, date_created→date
                    project = Project(
                        title=proj_data.title,
                        description=proj_data.description,
                        category=category,
                        source=ProjectSource.MANUAL,
                        tags=proj_data.tags,
                        links=[proj_data.url] if proj_data.url else [],
                        images=[proj_data.image_url] if proj_data.image_url else [],
                        date=datetime.now(timezone.utc)
                    )
                    projects.append(project)
                except Exception as e:
                    logger.warning(f"Error creating project: {e}", exc_info=True)
                    continue
            
            if not projects:
                return jsonify({'error': 'No valid projects provided'}), 400
            
            # Create portfolio
            portfolio = Portfolio(
                owner_name=request_data.owner.name,
                owner_email=request_data.owner.email,
                owner_title=request_data.owner.title,
                owner_bio=request_data.owner.bio,
                projects=projects,
                theme=request_data.theme,
                color_scheme=request_data.color_scheme,
                show_watermark=request_data.show_watermark
            )
            
            # Generate portfolio
            portfolio_id = str(uuid.uuid4())
            output_dir = os.path.join(STORAGE_DIR, portfolio_id)
            
            generator = PortfolioGenerator({'output_dir': output_dir})
            output_path = generator.generate(portfolio, portfolio_id)
            
            return jsonify({
                'success': True,
                'portfolio_id': portfolio_id,
                'download_url': f'/api/download/{portfolio_id}',
                'preview_url': f'/api/preview/{portfolio_id}',
                'project_count': len(projects),
                'message': 'Portfolio generated successfully'
            })
            
        except Exception as e:
            logger.error(f"Error generating portfolio: {e}", exc_info=True)
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/generate/auto', methods=['POST'])
    def generate_portfolio_auto():
        """Auto-generate portfolio from configured data sources.
        
        Request body:
        {
            "config": {
                "user": { ... },
                "google": { ... },
                "slack": { ... },
                ...
            }
        }
        
        Returns:
            JSON with portfolio_id and download URL
        """
        try:
            data = request.get_json()
            
            if not data or 'config' not in data:
                return jsonify({'error': 'Configuration required'}), 400
            
            # Save config to temporary file
            config_file = os.path.join(tempfile.gettempdir(), f'config_{uuid.uuid4()}.yaml')
            
            with open(config_file, 'w') as f:
                import yaml
                yaml.dump(data['config'], f)
            
            try:
                # Initialize necromancer with config
                necromancer = PortfolioNecromancer(config_file)
                
                # Generate portfolio ID
                portfolio_id = str(uuid.uuid4())
                
                # Override output directory
                necromancer.generator.config['output_dir'] = os.path.join(STORAGE_DIR, portfolio_id)
                
                # Generate portfolio
                output_path = necromancer.resurrect(portfolio_id)
                
                return jsonify({
                    'success': True,
                    'portfolio_id': portfolio_id,
                    'download_url': f'/api/download/{portfolio_id}',
                    'preview_url': f'/api/preview/{portfolio_id}',
                    'message': 'Portfolio generated successfully from data sources'
                })
                
            finally:
                # Clean up temp config file
                if os.path.exists(config_file):
                    os.remove(config_file)
                    
        except Exception as e:
            logger.error(f"Error in auto-generation: {e}", exc_info=True)
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/preview/<portfolio_id>', methods=['GET'])
    def preview_portfolio(portfolio_id: str):
        """Preview generated portfolio HTML.
        
        Args:
            portfolio_id: Unique portfolio identifier
            
        Returns:
            HTML content of the portfolio
        """
        try:
            portfolio_path = os.path.join(STORAGE_DIR, portfolio_id, 'index.html')
            
            if not os.path.exists(portfolio_path):
                return jsonify({'error': 'Portfolio not found'}), 404
            
            return send_file(portfolio_path, mimetype='text/html')
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/download/<portfolio_id>', methods=['GET'])
    def download_portfolio(portfolio_id: str):
        """Download generated portfolio as ZIP file.
        
        Args:
            portfolio_id: Unique portfolio identifier
            
        Returns:
            ZIP file containing the portfolio
        """
        try:
            portfolio_path = os.path.join(STORAGE_DIR, portfolio_id)
            
            if not os.path.exists(portfolio_path):
                return jsonify({'error': 'Portfolio not found'}), 404
            
            # Create ZIP file
            zip_path = os.path.join(tempfile.gettempdir(), f'{portfolio_id}.zip')
            shutil.make_archive(zip_path.replace('.zip', ''), 'zip', portfolio_path)
            
            return send_file(
                zip_path,
                mimetype='application/zip',
                as_attachment=True,
                download_name=f'portfolio_{portfolio_id}.zip'
            )
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/categories', methods=['GET'])
    def get_categories():
        """Get available project categories.
        
        Returns:
            JSON list of available categories
        """
        return jsonify({
            'categories': [cat.value for cat in ProjectCategory]
        })
    
    @app.route('/api/themes', methods=['GET'])
    def get_themes():
        """Get available themes and color schemes.
        
        Returns:
            JSON with available themes and color schemes
        """
        return jsonify({
            'themes': ['modern'],
            'color_schemes': ['blue', 'green', 'purple']
        })
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app


def run_server(host='0.0.0.0', port=5000, debug=False):
    """Run the Flask development server.
    
    Args:
        host: Host to bind to
        port: Port to bind to
        debug: Enable debug mode
    """
    app = create_app()
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_server(debug=True)
