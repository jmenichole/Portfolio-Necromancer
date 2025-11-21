# Portfolio Necromancer - Examples

This directory contains practical examples demonstrating how to use Portfolio Necromancer.

## Available Examples

### 1. API Example (`api_example.py`)

Demonstrates how to use the Portfolio Necromancer REST API to generate portfolios programmatically.

**Usage:**

```bash
# First, start the API server in a separate terminal
python -m portfolio_necromancer.api.server

# Then run the example
python examples/api_example.py
```

**What it does:**
- Checks API health
- Retrieves available categories and themes
- Generates a sample portfolio with 5 projects
- Displays preview and download URLs

**Features demonstrated:**
- Making API requests with Python
- Error handling
- Portfolio generation with custom data
- Working with API responses

### 2. CLI Demo (`../demo.py`)

The main demo script that showcases portfolio generation without API credentials.

**Usage:**

```bash
python demo.py
```

**What it does:**
- Creates 10 sample projects
- Generates AI summaries
- Creates a complete portfolio website
- Saves output to `demo_portfolio/demo/`

## Quick Start

The easiest way to get started is:

```bash
# Run the quick start script
chmod +x quickstart.sh
./quickstart.sh
```

This will:
1. Install all dependencies
2. Run tests to verify installation
3. Generate a demo portfolio
4. Optionally start the API server

## Creating Your Own Portfolio

### Option 1: Using the Web Dashboard

1. Start the server:
   ```bash
   python -m portfolio_necromancer.api.server
   ```

2. Open your browser to `http://localhost:5000`

3. Fill in your information and projects

4. Click "Generate Portfolio"

### Option 2: Using the Python API

```python
from portfolio_necromancer import PortfolioNecromancer
from portfolio_necromancer.models import Portfolio, Project, ProjectCategory, ProjectSource

# Create projects
projects = [
    Project(
        title="My Awesome Project",
        description="A groundbreaking application",
        category=ProjectCategory.CODE,
        source=ProjectSource.MANUAL,
        tags=["python", "web", "api"]
    )
]

# Create portfolio
portfolio = Portfolio(
    owner_name="Your Name",
    owner_email="you@example.com",
    owner_title="Developer",
    owner_bio="I build cool things",
    projects=projects
)

# Generate
from portfolio_necromancer.generator import PortfolioGenerator
generator = PortfolioGenerator({'output_dir': './my-portfolio'})
generator.generate(portfolio, 'my-portfolio')
```

### Option 3: Using the REST API

```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "owner": {
      "name": "Your Name",
      "email": "you@example.com",
      "title": "Developer"
    },
    "projects": [
      {
        "title": "My Project",
        "description": "Description",
        "category": "code",
        "tags": ["python"]
      }
    ]
  }'
```

### Option 4: Using JavaScript/Node.js

```javascript
const fetch = require('node-fetch');

const data = {
  owner: {
    name: 'Your Name',
    email: 'you@example.com',
    title: 'Developer'
  },
  projects: [
    {
      title: 'My Project',
      description: 'Description',
      category: 'code',
      tags: ['javascript', 'node']
    }
  ],
  theme: 'modern',
  color_scheme: 'blue'
};

fetch('http://localhost:5000/api/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(data)
})
  .then(res => res.json())
  .then(result => {
    console.log('Portfolio ID:', result.portfolio_id);
    console.log('Preview:', result.preview_url);
    console.log('Download:', result.download_url);
  });
```

## Advanced Examples

### Auto-Generation from Data Sources

If you have configured your data source credentials (Google, Slack, Figma):

```python
from portfolio_necromancer import PortfolioNecromancer

# Initialize with config file
necromancer = PortfolioNecromancer('config.yaml')

# Auto-generate from all configured sources
output_path = necromancer.resurrect()

print(f"Portfolio generated at: {output_path}")
```

### Customizing Themes and Colors

```python
portfolio = Portfolio(
    owner_name="Your Name",
    owner_email="you@example.com",
    owner_title="Designer",
    owner_bio="Creating beautiful experiences",
    projects=projects,
    theme="modern",           # Available: modern
    color_scheme="purple",    # Available: blue, green, purple
    show_watermark=False      # Pro feature
)
```

### Batch Processing

Generate multiple portfolios:

```python
users = [
    {"name": "User 1", "email": "user1@example.com", "projects": [...]},
    {"name": "User 2", "email": "user2@example.com", "projects": [...]},
]

for user in users:
    portfolio = Portfolio(
        owner_name=user["name"],
        owner_email=user["email"],
        projects=user["projects"]
    )
    
    generator = PortfolioGenerator({'output_dir': f'./portfolios/{user["name"]}'})
    generator.generate(portfolio)
```

## Tips and Best Practices

1. **Start with the demo**: Run `demo.py` to see what's possible
2. **Use the web dashboard**: It's the easiest way to get started
3. **Test with sample data**: Use the API example before creating your own
4. **Check the docs**: See `docs/API_GUIDE.md` for complete API reference
5. **Customize themes**: Edit CSS files in the templates directory to match your branding

## Troubleshooting

**Server won't start:**
- Check if port 5000 is already in use
- Try a different port: `python -m portfolio_necromancer.api.server --port 8080`

**API requests fail:**
- Ensure the server is running
- Check the URL is correct (http://localhost:5000)
- Verify Content-Type header is set

**Import errors:**
- Run `pip install -e .` to install the package
- Make sure you're in the project root directory

## Contributing

Want to add more examples? Great! Please:
1. Create a new example file
2. Add documentation to this README
3. Submit a pull request

---

**Happy portfolio building!** 🧟
