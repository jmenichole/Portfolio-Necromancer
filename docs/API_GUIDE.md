# Portfolio Necromancer - Fullstack API Guide

## Overview

Portfolio Necromancer now includes a complete fullstack web application with:
- **REST API** - Flask-based backend for portfolio generation
- **Web Dashboard** - Interactive UI for creating portfolios
- **Real-time Generation** - Generate portfolios through the web interface
- **Download & Preview** - View and download generated portfolios

## Quick Start

### 1. Install Dependencies

```bash
pip install -e .
```

### 2. Start the API Server

```bash
python -m portfolio_necromancer.api.server
```

Or with custom options:

```bash
python -m portfolio_necromancer.api.server --host 0.0.0.0 --port 8080 --debug
```

### 3. Access the Dashboard

Open your browser and navigate to:
```
http://localhost:5000/
```

## API Endpoints

### Health Check
```
GET /api/health
```

Returns API status and version information.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2025-11-21T06:00:00.000000+00:00"
}
```

### Generate Portfolio (Manual)
```
POST /api/generate
```

Generate a portfolio from manually provided project data.

**Request Body:**
```json
{
  "owner": {
    "name": "Your Name",
    "email": "you@example.com",
    "title": "Developer",
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
```

**Response:**
```json
{
  "success": true,
  "portfolio_id": "uuid-here",
  "download_url": "/api/download/uuid-here",
  "preview_url": "/api/preview/uuid-here",
  "project_count": 1,
  "message": "Portfolio generated successfully"
}
```

### Generate Portfolio (Auto)
```
POST /api/generate/auto
```

Auto-generate portfolio from configured data sources.

**Request Body:**
```json
{
  "config": {
    "user": {
      "name": "Your Name",
      "email": "you@example.com"
    },
    "google": {
      "credentials_file": "credentials.json"
    },
    "slack": {
      "token": "xoxb-your-token"
    }
  }
}
```

### Preview Portfolio
```
GET /api/preview/{portfolio_id}
```

Returns the generated portfolio HTML for preview.

### Download Portfolio
```
GET /api/download/{portfolio_id}
```

Downloads the portfolio as a ZIP file.

### Get Available Categories
```
GET /api/categories
```

**Response:**
```json
{
  "categories": ["Writing", "Design", "Code", "Miscellaneous Unicorn Work"]
}
```

### Get Available Themes
```
GET /api/themes
```

**Response:**
```json
{
  "themes": ["modern"],
  "color_schemes": ["blue", "green", "purple"]
}
```

## Using the Web Dashboard

### Manual Entry Mode

1. **Fill in your information:**
   - Name (required)
   - Email (required)
   - Title
   - Bio

2. **Add projects:**
   - Click "+ Add Project"
   - Fill in project details (title, description, category, tags)
   - Repeat for each project

3. **Customize:**
   - Select theme
   - Choose color scheme

4. **Generate:**
   - Click "🧟 Generate Portfolio"
   - Wait for generation to complete
   - Preview or download your portfolio

### Auto-Generate Mode

1. **Prepare configuration:**
   - Create a JSON configuration with your API credentials
   - Include data source settings

2. **Paste configuration:**
   - Switch to "Auto-Generate" tab
   - Paste your JSON config

3. **Generate:**
   - Click "🔮 Auto-Generate Portfolio"
   - The system will scrape your data sources
   - Preview or download the result

## Using the API Programmatically

### Python Example

```python
import requests

# Generate portfolio
url = "http://localhost:5000/api/generate"
data = {
    "owner": {
        "name": "John Doe",
        "email": "john@example.com",
        "title": "Fullstack Developer",
        "bio": "Passionate about building great software"
    },
    "projects": [
        {
            "title": "E-commerce Platform",
            "description": "A scalable e-commerce solution",
            "category": "code",
            "tags": ["python", "django", "react"],
            "url": "https://github.com/john/ecommerce"
        }
    ],
    "theme": "modern",
    "color_scheme": "blue"
}

response = requests.post(url, json=data)
result = response.json()

print(f"Portfolio ID: {result['portfolio_id']}")
print(f"Preview: http://localhost:5000{result['preview_url']}")
print(f"Download: http://localhost:5000{result['download_url']}")
```

### JavaScript Example

```javascript
// Generate portfolio
const url = 'http://localhost:5000/api/generate';
const data = {
  owner: {
    name: 'Jane Smith',
    email: 'jane@example.com',
    title: 'Designer',
    bio: 'Creating beautiful experiences'
  },
  projects: [
    {
      title: 'Brand Identity Design',
      description: 'Complete brand redesign',
      category: 'design',
      tags: ['branding', 'logo', 'ui'],
      url: 'https://behance.net/jane/project'
    }
  ],
  theme: 'modern',
  color_scheme: 'purple'
};

fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(data)
})
  .then(response => response.json())
  .then(result => {
    console.log('Portfolio ID:', result.portfolio_id);
    console.log('Preview:', result.preview_url);
    console.log('Download:', result.download_url);
  });
```

### cURL Example

```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "owner": {
      "name": "Alex Developer",
      "email": "alex@example.com",
      "title": "Software Engineer"
    },
    "projects": [
      {
        "title": "My Project",
        "description": "An amazing project",
        "category": "code",
        "tags": ["python", "api"]
      }
    ],
    "theme": "modern",
    "color_scheme": "green"
  }'
```

## Deployment

### Development Server

The built-in Flask development server is suitable for testing:

```bash
python -m portfolio_necromancer.api.server --debug
```

### Production Deployment

For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn

gunicorn -w 4 -b 0.0.0.0:5000 'portfolio_necromancer.api.app:create_app()'
```

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install -e .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "portfolio_necromancer.api.app:create_app()"]
```

Build and run:

```bash
docker build -t portfolio-necromancer .
docker run -p 5000:5000 portfolio-necromancer
```

## Environment Variables

- `SECRET_KEY` - Flask secret key (change in production)
- `PORT` - Server port (default: 5000)
- `DEBUG` - Enable debug mode (default: False)

## Security Considerations

1. **Change the secret key in production:**
   ```bash
   export SECRET_KEY="your-random-secret-key"
   ```

2. **Use HTTPS in production**

3. **Rate limiting** - Consider adding rate limiting for production

4. **CORS** - Configure CORS appropriately for your domain

## Troubleshooting

### Port Already in Use

```bash
# Use a different port
python -m portfolio_necromancer.api.server --port 8080
```

### API Not Accessible

Check firewall settings and ensure the server is running:

```bash
curl http://localhost:5000/api/health
```

### Portfolio Generation Fails

- Check request payload format
- Verify all required fields are provided
- Check server logs for detailed error messages

## API Testing

Run the test suite:

```bash
pytest tests/test_api.py -v
```

## Features

### ✅ Implemented

- REST API for portfolio generation
- Web dashboard interface
- Manual project entry
- Auto-generation from config
- Portfolio preview
- ZIP download
- Theme and color customization
- Comprehensive API tests

### 🔮 Future Enhancements

- User authentication
- Database storage for portfolios
- WebSocket for real-time progress
- Portfolio versioning
- Template marketplace
- Social media sharing
- Analytics dashboard
- API rate limiting
- Advanced customization options

## Contributing

Contributions to the API and dashboard are welcome! Please submit pull requests with:
- Comprehensive tests
- API documentation updates
- Security considerations

---

**Need Help?** Open an issue on GitHub or check the main [README.md](../README.md)
