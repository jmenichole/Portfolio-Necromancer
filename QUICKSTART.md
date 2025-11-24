# Quick Start Guide

Get your portfolio up and running in 5 minutes with proper Python environment isolation!

## Prerequisites

- **Python 3.8 or higher** ([Download here](https://www.python.org/downloads/))
- **pip package manager** (included with Python)
- **Basic command line knowledge**

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/jmenichole/Portfolio-Necromancer.git
cd Portfolio-Necromancer
```

### Step 2: Create Virtual Environment

**Why use a virtual environment?** It isolates this project's dependencies from your system Python and other projects, preventing version conflicts and keeping your system clean.

#### Option A: Using venv (Recommended)

```bash
# Create virtual environment
python -m venv .venv

# Activate it
# On macOS/Linux:
source .venv/bin/activate

# On Windows (Command Prompt):
.venv\Scripts\activate.bat

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

#### Option B: Using conda

```bash
# Create environment
conda create -n portfolio-necromancer python=3.11

# Activate it
conda activate portfolio-necromancer
```

**Important**: You'll need to activate your virtual environment every time you open a new terminal session to work on this project.

### Step 3: Install Dependencies

With your virtual environment activated (you should see `(.venv)` or `(portfolio-necromancer)` in your terminal prompt):

```bash
# Upgrade pip first
pip install --upgrade pip

# Install the package in editable mode
pip install -e .

# Verify installation
portfolio-necromancer --version
```

### Step 4: Install Optional Dependencies

If you plan to use specific features, install their dependencies:

```bash
# For AI-powered categorization
pip install -e ".[ai]"

# For all scraping sources
pip install -e ".[scraping]"

# For development
pip install -e ".[dev]"

# For everything
pip install -e ".[all]"
```

## Quick Demo

Want to see what Portfolio Necromancer can do? Run the demo:

```bash
# Make sure your virtual environment is activated!
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

Save this as `my_portfolio.py` and run:

```bash
python my_portfolio.py
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

## Managing Your Environment

### Deactivating the Virtual Environment

When you're done working:

```bash
deactivate
```

### Reactivating for Future Sessions

Every time you come back to work on your portfolio:

```bash
cd Portfolio-Necromancer

# venv users:
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# conda users:
conda activate portfolio-necromancer
```

### Updating Dependencies

If you pull new changes from the repository:

```bash
# With virtual environment activated
pip install --upgrade -e .
```

### Exporting Dependencies

To share your exact environment with others:

```bash
# Create requirements file
pip freeze > requirements-freeze.txt

# Others can install with:
pip install -r requirements-freeze.txt
```

### Cleaning Up

To completely remove the virtual environment:

```bash
# Deactivate first
deactivate

# Remove the directory
# venv users:
rm -rf .venv  # macOS/Linux
rmdir /s .venv  # Windows

# conda users:
conda env remove -n portfolio-necromancer
```

## What's Next?

1. **Customize the theme**: Edit CSS in `src/portfolio_necromancer/templates/assets/style.css`
2. **Add more projects**: Run the scraper again or add projects manually
3. **Deploy**: Upload the generated HTML to GitHub Pages, Netlify, or Vercel
4. **Go Pro**: Remove watermark and get unlimited projects (update feature flags in config.yaml)

## Common Issues

### "Command not found: portfolio-necromancer"

**Solution**: Your virtual environment isn't activated. Run the activation command for your platform (see Step 2 above).

### "No projects found"

- Check that at least one data source is enabled in `config.yaml`
- Verify your API credentials are correct
- Try running the demo first to ensure the system works

### "Module not found" / Import Errors

**Solution**: 
```bash
# Make sure virtual environment is activated
# Then reinstall
pip install --upgrade -e .
```

### "Permission denied" when installing

**Solution**: Don't use `sudo pip install`. Instead, make sure you're using a virtual environment (see Step 2).

### "API authentication failed"

- Double-check your API keys in `config.yaml`
- Ensure credentials files (like `credentials.json` for Google) are in the correct location
- Review the API setup guides in the main README

### Virtual Environment Not Activating (Windows PowerShell)

**Solution**: You may need to change the execution policy:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Python Version Conflicts

**Solution**: Specify the Python version explicitly:
```bash
# venv with specific Python version
python3.11 -m venv .venv

# conda with specific version
conda create -n portfolio-necromancer python=3.11
```

## Best Practices

✅ **Always activate your virtual environment** before running portfolio commands  
✅ **Keep your `.venv` folder** in `.gitignore` (already configured)  
✅ **Update pip regularly**: `pip install --upgrade pip`  
✅ **Use `requirements.txt`** for reproducible builds  
✅ **Document your Python version** in your README  

❌ **Never use `sudo pip install`**  
❌ **Don't commit virtual environment folders** to git  
❌ **Don't mix conda and venv** in the same project  

## Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Review example configuration in [config.example.yaml](config.example.yaml)
- Look at the [demo.py](demo.py) for usage examples
- Open an issue on GitHub

---

**Pro Tip**: Create an alias in your shell config to quickly activate your environment:
```bash
# Add to ~/.bashrc or ~/.zshrc
alias pn='cd ~/path/to/Portfolio-Necromancer && source .venv/bin/activate'
```

Then just type `pn` to jump into your portfolio workspace with the environment ready!

This version prevents dependency conflicts, makes the project more maintainable, and follows Python packaging best practices!
