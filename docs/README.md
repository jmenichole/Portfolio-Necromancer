# GitHub Pages Setup

This directory contains the GitHub Pages landing page for Portfolio Necromancer.

## Viewing the Landing Page

Once GitHub Pages is enabled for this repository, the landing page will be available at:
- **URL**: `https://jmenichole.github.io/Portfolio-Necromancer/`

## Local Development

To preview the landing page locally:

1. Navigate to this directory:
   ```bash
   cd docs
   ```

2. Start a simple HTTP server:
   ```bash
   # Python 3
   python3 -m http.server 8000
   
   # Or with Node.js
   npx http-server -p 8000
   ```

3. Open in browser:
   ```
   http://localhost:8000
   ```

## Enabling GitHub Pages

To enable GitHub Pages for this repository:

1. Go to repository **Settings**
2. Navigate to **Pages** section (under "Code and automation")
3. Under **Source**, select:
   - Source: `Deploy from a branch`
   - Branch: `main` (or your default branch)
   - Folder: `/docs`
4. Click **Save**
5. Wait a few minutes for deployment
6. Visit `https://jmenichole.github.io/Portfolio-Necromancer/`

## Files

- `index.html` - Main landing page with project overview, features, and getting started
- `style.css` - Styles for the landing page
- `README.md` - This file (setup instructions)

## Customization

To customize the landing page:

1. Edit `index.html` for content changes
2. Edit `style.css` for styling changes
3. Test locally before committing
4. Push to main branch to deploy

## Features

The landing page includes:
- Hero section with call-to-action
- Problem/solution overview
- Feature showcase
- Live demo instructions
- Getting started guide
- Integration documentation
- Pricing information
- Links to full documentation

## Design

- Modern, responsive design
- Mobile-friendly
- Gradient hero section
- Card-based layout
- Clean typography
- Smooth animations
