# Portfolio Necromancer 🧟

> Resurrect your portfolio from the digital wreckage of your hustle

Portfolio Necromancer is an automated tool that scrapes your inbox, Google Drive, Docs, Figma links, Slack threads, and old screenshots to auto-build a stunning portfolio site. Perfect for freelancers and creators who are too busy actually doing great work to maintain a portfolio.

**🌐 [View Landing Page](https://jmenichole.github.io/Portfolio-Necromancer/)** | **📚 [Integration Guide](INTEGRATIONS.md)** | **⚡ [Quick Start](QUICKSTART.md)**

## ✨ Features

- **🔍 Multi-Source Scraping**: Automatically discovers your work from:
  - Gmail/Email attachments
  - Google Drive files
  - Google Docs
  - Figma design files
  - Slack conversations
  - Screenshot folders

- **🏷️ Smart Categorization**: AI-powered auto-categorization into:
  - Writing
  - Design
  - Code
  - Miscellaneous Unicorn Work

- **✨ AI-Generated Summaries**: Professional project descriptions that make you sound impressive:
  > "In this project, [your name] skillfully wrangled a broken system to deliver [miracle]."

- **🎨 Beautiful Portfolio Sites**: Generates modern, responsive static websites ready to deploy

- **💎 Pro Features** (Monetization Ready):
  - Custom domains
  - Custom branding
  - Remove watermark
  - Unlimited projects (free tier: 20 projects)
  - Advanced analytics

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/jmenichole/Portfolio-Necromancer.git
cd Portfolio-Necromancer

# Install dependencies
pip install -r requirements.txt

# Or install as a package
pip install -e .
```

### Initial Setup

1. Create your configuration file:
```bash
portfolio-necromancer --init
```

2. Edit `config.yaml` with your credentials and preferences:
```yaml
user:
  name: "Your Name"
  email: "your.email@example.com"
  title: "Freelancer / Developer / Designer"
  bio: "Short bio about yourself"

ai:
  api_key: "your-openai-api-key"  # For AI categorization and summaries

# Configure your data sources
google:
  credentials_file: "credentials.json"

slack:
  token: "xoxb-your-slack-bot-token"

figma:
  access_token: "your-figma-access-token"
```

3. Set up data source credentials:
   - **Google**: Follow [Google API setup guide](https://developers.google.com/workspace/guides/create-credentials)
   - **Slack**: Create a Slack app and get a bot token
   - **Figma**: Get your personal access token from Figma settings
   - **OpenAI**: Get an API key from [OpenAI](https://platform.openai.com/api-keys)
   
   📖 **See [INTEGRATIONS.md](INTEGRATIONS.md) for detailed setup instructions for all integrations**

### Generate Your Portfolio

```bash
# Generate with default settings
portfolio-necromancer

# Use custom config
portfolio-necromancer --config my-config.yaml

# Custom output directory name
portfolio-necromancer --output awesome-portfolio
```

The generated portfolio will be in `./generated_portfolios/` by default.

## 📖 Usage

### Basic Usage

```python
from portfolio_necromancer import PortfolioNecromancer

# Initialize
necromancer = PortfolioNecromancer('config.yaml')

# Generate portfolio
output_path = necromancer.resurrect()

print(f"Portfolio generated at: {output_path}")
```

### Advanced Usage

```python
from portfolio_necromancer import PortfolioNecromancer, Portfolio, Project
from portfolio_necromancer.models import ProjectCategory, ProjectSource

# Create custom project
project = Project(
    title="My Awesome Project",
    description="A groundbreaking application",
    category=ProjectCategory.CODE,
    source=ProjectSource.MANUAL,
    tags=["python", "web", "api"]
)

# Initialize and add custom projects
necromancer = PortfolioNecromancer()
portfolio = Portfolio(
    owner_name="Your Name",
    owner_email="you@example.com",
    owner_title="Developer",
    owner_bio="I build cool things",
    projects=[project]
)

# Generate with custom portfolio
from portfolio_necromancer.generator import PortfolioGenerator
generator = PortfolioGenerator({'output_dir': './my-portfolio'})
generator.generate(portfolio, 'custom-name')
```

## 🎨 Customization

### Themes and Colors

Supported themes:
- `modern` (default)

Supported color schemes:
- `blue` (default)
- `green`
- `purple`

Configure in `config.yaml`:
```yaml
portfolio:
  theme: "modern"
  color_scheme: "blue"
```

### Custom Templates

Templates are in `src/portfolio_necromancer/templates/`. You can:
1. Modify existing templates (HTML/CSS)
2. Add new themes
3. Customize styling in `assets/style.css`

## 🔧 Configuration

### Data Source Settings

```yaml
scraping:
  email:
    enabled: true
    max_messages: 100
    date_range_days: 365
  
  drive:
    enabled: true
    max_files: 50
  
  slack:
    enabled: true
    max_messages: 100
  
  figma:
    enabled: true
    max_projects: 20
  
  screenshots:
    enabled: true
    folder_path: "./screenshots"
```

### Feature Flags

```yaml
features:
  custom_domain: false          # Pro feature
  custom_branding: false        # Pro feature
  remove_watermark: false       # Pro feature
  unlimited_projects: false     # Free tier: 20 projects
  advanced_analytics: false     # Pro feature
```

## 💰 Monetization Model

Portfolio Necromancer supports a freemium model:

**Free Tier:**
- Up to 20 projects
- Basic themes
- Portfolio Necromancer watermark

**Pro Tier:**
- Unlimited projects
- Custom domains
- Custom branding
- Remove watermark
- Priority support
- Advanced analytics

Enable pro features in `config.yaml`:
```yaml
features:
  unlimited_projects: true
  custom_branding: true
  remove_watermark: true
  custom_domain: "yourdomain.com"
```

## 🎯 Target Audience

Perfect for:
- **Freelancers** who are too busy working to update their portfolio
- **Developers** with projects scattered across GitHub, email, and Slack
- **Designers** with work across Figma, Drive, and screenshots
- **Writers** with articles spread across docs and emails
- **Anyone** who does great work but never documents it

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Built for the hustle culture generation
- Inspired by every freelancer who's ever said "I'll update my portfolio tomorrow"
- Powered by AI to make your work sound as impressive as it actually is

---

**Remember:** You're not lazy, you're just too busy being awesome. Let Portfolio Necromancer handle the portfolio. 🚀
