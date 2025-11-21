"""
Example: Using Portfolio Necromancer API
This script demonstrates how to use the Portfolio Necromancer API
to generate portfolios programmatically.
"""

import requests
import json
import time

# API Base URL
API_URL = "http://localhost:5000"


def check_api_health():
    """Check if the API is running."""
    try:
        response = requests.get(f"{API_URL}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✓ API is healthy")
            print(f"  Version: {data['version']}")
            return True
        else:
            print("✗ API is not responding correctly")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Cannot connect to API: {e}")
        print(f"  Make sure the server is running: python -m portfolio_necromancer.api.server")
        return False


def generate_portfolio():
    """Generate a portfolio using the API."""
    print("\n📝 Generating portfolio...")
    
    # Portfolio data
    portfolio_data = {
        "owner": {
            "name": "Jane Developer",
            "email": "jane@example.com",
            "title": "Fullstack Developer & Designer",
            "bio": "Passionate about creating beautiful and functional web applications. "
                   "5+ years of experience in fullstack development."
        },
        "projects": [
            {
                "title": "E-commerce Platform",
                "description": "A scalable e-commerce solution built with Python, Django, and React. "
                              "Features include user authentication, payment processing, and real-time inventory.",
                "category": "code",
                "tags": ["python", "django", "react", "postgresql", "api"],
                "url": "https://github.com/jane/ecommerce"
            },
            {
                "title": "Task Management App",
                "description": "A collaborative task management application with real-time updates. "
                              "Built with Node.js, Express, and Vue.js.",
                "category": "code",
                "tags": ["javascript", "node", "vue", "websocket"],
                "url": "https://github.com/jane/taskmanager"
            },
            {
                "title": "Mobile Banking UI",
                "description": "Modern and intuitive mobile banking interface design. "
                              "Created with Figma, focusing on accessibility and user experience.",
                "category": "design",
                "tags": ["figma", "ui", "ux", "mobile", "fintech"],
                "url": "https://figma.com/jane/banking-ui"
            },
            {
                "title": "Blog Platform",
                "description": "A lightweight blog platform with markdown support and SEO optimization. "
                              "Built with Flask and deployed on AWS.",
                "category": "code",
                "tags": ["python", "flask", "aws", "markdown"],
                "url": "https://github.com/jane/blog"
            },
            {
                "title": "Technical Writing Portfolio",
                "description": "Collection of technical articles on web development, DevOps, and cloud computing. "
                              "Published on Medium and personal blog.",
                "category": "writing",
                "tags": ["technical writing", "devops", "cloud"],
                "url": "https://medium.com/@jane"
            }
        ],
        "theme": "modern",
        "color_scheme": "purple"
    }
    
    # Make API request
    try:
        response = requests.post(
            f"{API_URL}/api/generate",
            json=portfolio_data,
            headers={"Content-Type": "application/json"},
            timeout=60  # Portfolio generation can take time
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Portfolio generated successfully!")
            print(f"  Portfolio ID: {result['portfolio_id']}")
            print(f"  Projects: {result['project_count']}")
            print(f"  Preview: {API_URL}{result['preview_url']}")
            print(f"  Download: {API_URL}{result['download_url']}")
            return result
        else:
            print(f"✗ Failed to generate portfolio: {response.status_code}")
            print(f"  Error: {response.json()}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Request failed: {e}")
        return None


def get_available_options():
    """Get available categories and themes."""
    print("\n🎨 Available customization options:")
    
    # Get categories
    try:
        response = requests.get(f"{API_URL}/api/categories", timeout=5)
        if response.status_code == 200:
            categories = response.json()['categories']
            print(f"  Categories: {', '.join(categories)}")
    except:
        pass
    
    # Get themes
    try:
        response = requests.get(f"{API_URL}/api/themes", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  Themes: {', '.join(data['themes'])}")
            print(f"  Color Schemes: {', '.join(data['color_schemes'])}")
    except:
        pass


def main():
    """Main function."""
    print("🧟 Portfolio Necromancer API Example")
    print("=" * 50)
    
    # Check API health
    if not check_api_health():
        return
    
    # Get available options
    get_available_options()
    
    # Generate portfolio
    result = generate_portfolio()
    
    if result:
        print("\n" + "=" * 50)
        print("✅ Success!")
        print("\nNext steps:")
        print(f"  1. Open {API_URL}{result['preview_url']} to preview")
        print(f"  2. Download from {API_URL}{result['download_url']}")
        print("  3. Deploy to GitHub Pages, Netlify, or Vercel")
        print("=" * 50)


if __name__ == "__main__":
    main()
