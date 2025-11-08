# Portfolio Necromancer - Integrations Guide

This document provides detailed information about all the integrations available in Portfolio Necromancer, including setup instructions, requirements, and troubleshooting tips.

## Overview

Portfolio Necromancer can integrate with multiple platforms to automatically discover and import your projects. **All integrations are optional** - you can start with manual projects or the demo, then add integrations as needed.

## Table of Contents

1. [Quick Reference](#quick-reference)
2. [Google APIs](#google-apis)
3. [Slack](#slack)
4. [Figma](#figma)
5. [OpenAI](#openai)
6. [Local Screenshots](#local-screenshots)
7. [Configuration](#configuration)
8. [Troubleshooting](#troubleshooting)

---

## Quick Reference

| Integration | Purpose | Required For | Setup Time | API Cost |
|------------|---------|--------------|------------|----------|
| **OpenAI** | AI categorization & summaries | Best experience | 5 mins | Pay per use |
| **Google APIs** | Gmail, Drive, Docs | Email/file scraping | 15 mins | Free tier |
| **Slack** | Message/file discovery | Slack projects | 10 mins | Free |
| **Figma** | Design file access | Design projects | 5 mins | Free |
| **Screenshots** | Local file scanning | Local images | 1 min | Free |

---

## Google APIs

### What It Enables

- **Gmail Integration**: Scrape project-related emails and attachments
- **Google Drive**: Access files, presentations, and documents
- **Google Docs**: Import document content and metadata

### Prerequisites

- A Google account
- Access to Google Cloud Console
- 15 minutes setup time

### Setup Instructions

#### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Create Project" or select existing project
3. Name your project (e.g., "Portfolio Necromancer")

#### Step 2: Enable Required APIs

1. Navigate to "APIs & Services" → "Library"
2. Enable the following APIs:
   - **Gmail API** (for email scraping)
   - **Google Drive API** (for file access)
   - **Google Docs API** (for document access)

#### Step 3: Create Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Configure consent screen if prompted:
   - User Type: External (for personal use)
   - Add your email as test user
4. Application type: "Desktop app"
5. Download the credentials JSON file
6. Rename it to `credentials.json`
7. Place it in your Portfolio Necromancer directory

#### Step 4: Configure Portfolio Necromancer

In your `config.yaml`:

```yaml
google:
  credentials_file: "credentials.json"
  
scraping:
  email:
    enabled: true
    max_messages: 100
    date_range_days: 365
    keywords:
      - "project"
      - "design"
      - "deliverable"
      - "final"
      - "attachment"
  
  drive:
    enabled: true
    max_files: 50
    file_types:
      - "presentation"
      - "document"
      - "pdf"
      - "image"
```

#### Step 5: First Run Authentication

1. Run Portfolio Necromancer
2. A browser window will open for authorization
3. Sign in with your Google account
4. Grant requested permissions
5. A `token.json` file will be created automatically

### API Quotas & Limits

- **Gmail API**: 1 billion quota units/day (free tier)
- **Drive API**: 1 billion queries/day (free tier)
- **Docs API**: 300 read requests/minute (free tier)

These limits are sufficient for typical use cases.

### Troubleshooting

**Issue**: "Invalid credentials" error
- **Solution**: Re-download credentials.json from Google Cloud Console
- Ensure the file is named exactly `credentials.json`

**Issue**: "Access denied" during OAuth
- **Solution**: Add your email as a test user in OAuth consent screen

**Issue**: "Quota exceeded"
- **Solution**: Reduce `max_messages` and `max_files` in config
- Wait 24 hours for quota reset

---

## Slack

### What It Enables

- Search for project-related conversations
- Extract shared files and attachments
- Discover project URLs and links
- Preserve thread context

### Prerequisites

- Slack workspace access
- Permission to create apps
- 10 minutes setup time

### Setup Instructions

#### Step 1: Create a Slack App

1. Go to [Slack API](https://api.slack.com/apps)
2. Click "Create New App" → "From scratch"
3. Name: "Portfolio Necromancer"
4. Select your workspace

#### Step 2: Configure Bot Permissions

1. Navigate to "OAuth & Permissions"
2. Under "Scopes" → "Bot Token Scopes", add:
   - `channels:history` - Read public channel messages
   - `channels:read` - View basic channel info
   - `files:read` - View files shared in channels
   - `search:read` - Search workspace content
   - `users:read` - View people in workspace

#### Step 3: Install App to Workspace

1. Click "Install to Workspace"
2. Review and authorize permissions
3. Copy the "Bot User OAuth Token" (starts with `xoxb-`)

#### Step 4: Configure Portfolio Necromancer

In your `config.yaml`:

```yaml
slack:
  token: "xoxb-your-slack-bot-token-here"
  
scraping:
  slack:
    enabled: true
    max_messages: 100
    search_keywords:
      - "project"
      - "shipped"
      - "launched"
      - "design"
      - "prototype"
    channels:
      - "general"
      - "projects"
      - "design"
    # Or leave empty to search all channels
```

#### Step 5: Invite Bot to Channels

For the bot to access channel history:

```
/invite @Portfolio Necromancer
```

Run this in each channel you want to scrape.

### API Rate Limits

- **Tier 2**: 20+ requests per minute
- **Search**: 20 requests per minute
- Sufficient for typical portfolio generation

### Troubleshooting

**Issue**: "not_in_channel" error
- **Solution**: Invite the bot to the channel with `/invite @Portfolio Necromancer`

**Issue**: "missing_scope" error
- **Solution**: Add required scopes in OAuth & Permissions, reinstall app

**Issue**: No messages found
- **Solution**: Verify bot has access to channels
- Check search keywords match your actual conversations

---

## Figma

### What It Enables

- Access design files and projects
- Generate thumbnails from designs
- Extract file metadata and descriptions
- Import design work automatically

### Prerequisites

- Figma account (free or paid)
- 5 minutes setup time

### Setup Instructions

#### Step 1: Generate Personal Access Token

1. Log in to [Figma](https://www.figma.com)
2. Go to Account Settings → Personal Access Tokens
3. Click "Create new token"
4. Name: "Portfolio Necromancer"
5. Copy the token (starts with `figd_`)

#### Step 2: Configure Portfolio Necromancer

In your `config.yaml`:

```yaml
figma:
  access_token: "figd_your-figma-access-token-here"
  
scraping:
  figma:
    enabled: true
    max_projects: 20
    include_drafts: false
    thumbnail_size: "medium"  # small, medium, large
```

#### Step 3: Usage

Portfolio Necromancer will automatically:
- Scan your Figma teams and projects
- Generate thumbnails for each design
- Extract project names and descriptions
- Categorize as "Design" projects

### API Rate Limits

- **Rate limit**: 600 requests per minute
- More than sufficient for portfolio generation

### Troubleshooting

**Issue**: "Invalid token" error
- **Solution**: Regenerate token in Figma settings
- Ensure token is copied correctly (no extra spaces)

**Issue**: "No projects found"
- **Solution**: Ensure you have design files in your Figma account
- Check that files aren't in trash

**Issue**: Thumbnails not generating
- **Solution**: Verify files have at least one frame
- Try different `thumbnail_size` setting

---

## OpenAI

### What It Enables

- **AI Categorization**: Intelligently sort projects into categories
- **Summary Generation**: Create professional project descriptions
- **Context Understanding**: Better project interpretation

### Prerequisites

- OpenAI account
- Credit card on file (usage-based pricing)
- 5 minutes setup time

### Setup Instructions

#### Step 1: Get API Key

1. Go to [OpenAI Platform](https://platform.openai.com)
2. Sign up or log in
3. Navigate to API Keys
4. Click "Create new secret key"
5. Name: "Portfolio Necromancer"
6. Copy the key (starts with `sk-`)

#### Step 2: Configure Portfolio Necromancer

In your `config.yaml`:

```yaml
ai:
  api_key: "sk-your-openai-api-key-here"
  model: "gpt-3.5-turbo"  # Cost-effective option
  # Or use "gpt-4" for better results (more expensive)
  
  categorization:
    enabled: true
    confidence_threshold: 0.7
  
  summarization:
    enabled: true
    tone: "professional"  # professional, casual, enthusiastic
    length: "medium"      # short, medium, long
```

#### Step 3: Usage

Portfolio Necromancer will use OpenAI for:
- Categorizing projects based on content
- Generating impressive summaries
- Creating project descriptions

### Pricing (as of 2024)

- **GPT-3.5-Turbo**: ~$0.002 per 1K tokens
- **Typical portfolio (20 projects)**: ~$0.10-0.50
- **GPT-4**: More expensive but higher quality

### Fallback Behavior

If OpenAI is unavailable or disabled:
- Rule-based categorization kicks in
- Template-based summaries are used
- Portfolio generation still works

### Troubleshooting

**Issue**: "Insufficient credits" error
- **Solution**: Add credits to your OpenAI account
- Check billing settings

**Issue**: "Rate limit exceeded"
- **Solution**: Wait a few minutes and retry
- Consider upgrading OpenAI tier

**Issue**: Poor categorization
- **Solution**: Lower `confidence_threshold` in config
- Provide better project descriptions/context

---

## Local Screenshots

### What It Enables

- Scan local folders for project images
- Automatic image metadata extraction
- Include screenshots in portfolio

### Prerequisites

- Local folder with images
- No API keys needed
- 1 minute setup time

### Setup Instructions

In your `config.yaml`:

```yaml
scraping:
  screenshots:
    enabled: true
    folder_path: "./screenshots"  # Or absolute path
    # Supports multiple folders:
    # folder_paths:
    #   - "/Users/you/Desktop/Projects"
    #   - "/Users/you/Pictures/Work"
    
    file_extensions:
      - ".png"
      - ".jpg"
      - ".jpeg"
      - ".gif"
    
    recursive: true  # Scan subdirectories
    min_width: 400   # Minimum image width
    min_height: 300  # Minimum image height
```

### Supported Formats

- PNG, JPEG, JPG, GIF
- Automatically extracts dimensions
- Filename-based categorization

### Troubleshooting

**Issue**: No images found
- **Solution**: Check folder path is correct
- Verify folder contains supported image formats

**Issue**: Too many images
- **Solution**: Increase `min_width` and `min_height`
- Use more specific folder paths

---

## Configuration

### Complete Example Config

See [config.example.yaml](config.example.yaml) for a fully annotated configuration file.

### Environment Variables

You can also use environment variables instead of config file:

```bash
export OPENAI_API_KEY="sk-..."
export GOOGLE_CREDENTIALS="path/to/credentials.json"
export SLACK_TOKEN="xoxb-..."
export FIGMA_TOKEN="figd_..."
```

### Security Best Practices

1. **Never commit `config.yaml` to git** (already in .gitignore)
2. **Use environment variables** for production
3. **Rotate API keys** regularly
4. **Use separate keys** for dev/prod
5. **Limit API permissions** to minimum required

---

## Troubleshooting

### General Issues

**Portfolio generation fails**
1. Check config.yaml syntax (valid YAML)
2. Verify all API keys are valid
3. Run with verbose mode: `portfolio-necromancer --verbose`
4. Check logs in `portfolio-necromancer.log`

**No projects found**
1. Verify at least one data source is enabled
2. Check search keywords match your content
3. Try running the demo first: `python demo.py`
4. Test with manual projects

**Slow generation**
1. Reduce `max_messages`, `max_files` limits
2. Disable unused data sources
3. Use local caching (enabled by default)

### Getting Help

- **Documentation**: Check [README.md](README.md)
- **Examples**: See [demo.py](demo.py)
- **Issues**: Open on [GitHub](https://github.com/jmenichole/Portfolio-Necromancer/issues)
- **Quick Start**: See [QUICKSTART.md](QUICKSTART.md)

---

## Integration Comparison

### Which Integrations Do You Need?

**For Developers:**
- ✅ Google (Gmail for project emails)
- ✅ Slack (team conversations)
- ⚠️ Figma (if you do design work)
- ✅ OpenAI (for summaries)

**For Designers:**
- ✅ Figma (your design files)
- ✅ Google Drive (mockups, exports)
- ⚠️ Slack (if applicable)
- ✅ OpenAI (for descriptions)

**For Writers:**
- ✅ Google Docs (articles, drafts)
- ✅ Gmail (published links)
- ⚠️ Slack (if applicable)
- ✅ OpenAI (for summaries)

**For Everyone:**
- ✅ Screenshots (always useful)
- ✅ OpenAI (best experience)

### Starting Simple

**Recommended progression:**

1. **Start**: Run demo (`python demo.py`)
2. **Basic**: Add manual projects
3. **Automated**: Add OpenAI for AI features
4. **Full**: Add relevant data sources one at a time

---

## Future Integrations

Potential integrations in development:

- **GitHub**: Automatically import code repositories
- **Behance/Dribbble**: Import design portfolios
- **Medium/Substack**: Import written articles
- **LinkedIn**: Import experience/projects
- **Twitter**: Import threads showcasing work
- **Notion**: Import project databases

Vote for integrations or contribute at [GitHub Issues](https://github.com/jmenichole/Portfolio-Necromancer/issues).

---

## Summary

Portfolio Necromancer supports 5 main integrations, all optional:

1. **Google APIs** - Email, Drive, Docs (most comprehensive)
2. **Slack** - Team conversations and files
3. **Figma** - Design files and mockups
4. **OpenAI** - AI categorization and summaries (highly recommended)
5. **Local Screenshots** - Scan image folders (easiest)

Start with what's easiest for you, then expand as needed. The tool works perfectly fine with just manual projects or the demo!
