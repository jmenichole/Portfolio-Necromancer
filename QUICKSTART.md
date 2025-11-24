# Quick Start Guide

Get your portfolio up and running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

```bash
# Clone the repository
git clone https://github.com/jmenichole/Portfolio-Necromancer.git
cd Portfolio-Necromancer

# Install the package
pip install -e .
```

## Quick Demo

Want to see what Portfolio Necromancer can do? Run the demo:

```bash
python demo.py
```

This will generate a sample portfolio with 10 projects in `demo_portfolio/demo/`. Open `demo_portfolio/demo/index.html` in your browser to see the result!

**Want to deploy this demo portfolio online?** See [GITHUB_PAGES_SETUP.md](GITHUB_PAGES_SETUP.md#deploying-demo-portfolio-output) for instructions on deploying to GitHub Pages.

## Setup for Your Portfolio

### 1. Create Configuration

```bash
portfolio-necromancer --init
```

This creates a `config.yaml` file with default settings.

### 2. Edit Configuration

Open `config.yaml` and update your information:

```yaml
user:
  name: "Your Name"
  email: "your.email@example.com"
  title: "Your Title"
  bio: "Your bio"
```

### 3. Optional: Add API Keys

For AI-powered features, add your OpenAI API key:

```yaml
ai:
  api_key: "sk-your-openai-key"
```

For data scraping, add credentials for:
- **Google APIs**: Follow [this guide](https://developers.google.com/workspace/guides/create-credentials)
- **Slack**: Create a Slack app and add bot token
- **Figma**: Get token from Figma account settings

### 4. Generate Portfolio

#### Without Data Sources (Manual Projects)

You can start without API credentials by using the demo script as a template:

```python
from portfolio_necromancer import PortfolioNecromancer
from portfolio_necromancer.models import Portfolio, Project, ProjectCategory, ProjectSource

# Create manual projects
projects = [
    Project(
        title="My Awesome Project",
        description="Description of your project",
        category=ProjectCategory.CODE,
        source=ProjectSource.MANUAL,
        tags=["python", "web"]
    )
]

# Create portfolio
portfolio = Portfolio(
    owner_name="Your Name",
    owner_email="you@example.com",
    owner_title="Developer",
    owner_bio="Your bio",
    projects=projects
)

# Generate
from portfolio_necromancer.generator import PortfolioGenerator
generator = PortfolioGenerator({'output_dir': './my_portfolio'})
generator.generate(portfolio)
```

#### With Data Sources

Once you have API credentials configured:

```bash
portfolio-necromancer
```

This will:
1. Scrape all configured data sources
2. Categorize projects with AI
3. Generate summaries
4. Create your portfolio website

## View Your Portfolio

After generation, open the `index.html` file in your browser:

```bash
# On macOS
open generated_portfolios/portfolio_*/index.html

# On Linux
xdg-open generated_portfolios/portfolio_*/index.html

# On Windows
start generated_portfolios/portfolio_*/index.html
```

## What's Next?

1. **Customize the theme**: Edit CSS in `src/portfolio_necromancer/templates/assets/style.css`
2. **Add more projects**: Run the scraper again or add projects manually
3. **Deploy**: Upload the generated HTML to GitHub Pages, Netlify, or Vercel
4. **Go Pro**: Remove watermark and get unlimited projects (update feature flags in config.yaml)

## Common Issues

### "No projects found"

- Check that at least one data source is enabled in `config.yaml`
- Verify your API credentials are correct
- Try running the demo first to ensure the system works

### "Module not found"

Make sure you installed the package:
```bash
pip install -e .
```

### "API authentication failed"

- Double-check your API keys in `config.yaml`
- Ensure credentials files (like `credentials.json` for Google) are in the correct location
- Review the API setup guides in the main README

## Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Review example configuration in [config.example.yaml](config.example.yaml)
- Look at the [demo.py](demo.py) for usage examples
- Open an issue on GitHub

---

**Pro Tip**: Start with the demo, then gradually add your own data sources!
