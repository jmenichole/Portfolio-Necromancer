"""
Test Portfolio Necromancer API
"""

import unittest
import json
import tempfile
import os
from portfolio_necromancer.api.app import create_app


class TestPortfolioAPI(unittest.TestCase):
    """Test suite for Portfolio Necromancer API."""
    
    def setUp(self):
        """Set up test client."""
        self.app = create_app({'TESTING': True})
        self.client = self.app.test_client()
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('version', data)
        self.assertIn('timestamp', data)
    
    def test_get_categories(self):
        """Test getting available categories."""
        response = self.client.get('/api/categories')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('categories', data)
        self.assertIsInstance(data['categories'], list)
        self.assertIn('Code', data['categories'])
        self.assertIn('Design', data['categories'])
    
    def test_get_themes(self):
        """Test getting available themes."""
        response = self.client.get('/api/themes')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('themes', data)
        self.assertIn('color_schemes', data)
        self.assertIn('modern', data['themes'])
        self.assertIn('blue', data['color_schemes'])
    
    def test_generate_portfolio_missing_data(self):
        """Test portfolio generation with missing data."""
        response = self.client.post(
            '/api/generate',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_generate_portfolio_success(self):
        """Test successful portfolio generation."""
        payload = {
            'owner': {
                'name': 'Test User',
                'email': 'test@example.com',
                'title': 'Developer',
                'bio': 'Test bio'
            },
            'projects': [
                {
                    'title': 'Test Project',
                    'description': 'A test project',
                    'category': 'code',
                    'tags': ['python', 'test']
                }
            ],
            'theme': 'modern',
            'color_scheme': 'blue'
        }
        
        response = self.client.post(
            '/api/generate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('portfolio_id', data)
        self.assertIn('download_url', data)
        self.assertIn('preview_url', data)
        self.assertEqual(data['project_count'], 1)
    
    def test_generate_portfolio_invalid_owner(self):
        """Test portfolio generation with invalid owner data."""
        payload = {
            'owner': {
                'name': 'Test User'
                # Missing email
            },
            'projects': [
                {
                    'title': 'Test Project',
                    'category': 'code'
                }
            ]
        }
        
        response = self.client.post(
            '/api/generate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_dashboard_loads(self):
        """Test that dashboard HTML loads."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Portfolio Necromancer', response.data)


if __name__ == '__main__':
    unittest.main()
