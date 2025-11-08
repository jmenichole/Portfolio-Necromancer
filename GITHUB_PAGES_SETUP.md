# GitHub Pages Deployment Guide

This guide will help you enable GitHub Pages for the Portfolio Necromancer project to make the landing page publicly accessible.

## Quick Setup (5 minutes)

### Step 1: Enable GitHub Pages

1. Go to your repository: https://github.com/jmenichole/Portfolio-Necromancer
2. Click on **Settings** tab
3. Scroll down to **Pages** section (under "Code and automation")
4. Under **Build and deployment**:
   - **Source**: Select "Deploy from a branch"
   - **Branch**: Select `main` (or your default branch)
   - **Folder**: Select `/docs`
5. Click **Save**

### Step 2: Wait for Deployment

- GitHub will automatically build and deploy your site
- This usually takes 1-3 minutes
- You'll see a message: "Your site is live at `https://jmenichole.github.io/Portfolio-Necromancer/`"

### Step 3: Access Your Landing Page

Once deployed, your landing page will be available at:
- **URL**: https://jmenichole.github.io/Portfolio-Necromancer/

## What Was Created

### Landing Page Features
- ✅ Modern, responsive design
- ✅ Hero section with call-to-action
- ✅ Problem/solution presentation
- ✅ Feature showcase (6 key features)
- ✅ Live demo instructions
- ✅ Getting started guide
- ✅ Integration overview
- ✅ Pricing comparison
- ✅ Documentation links
- ✅ Mobile-friendly

### Files Created
- `docs/index.html` - Main landing page
- `docs/style.css` - Styling and layout
- `docs/README.md` - Setup documentation
- `INTEGRATIONS.md` - Complete integration guide

## Customization

### Update Content
To modify the landing page:

1. Edit `docs/index.html` for content changes
2. Edit `docs/style.css` for styling changes
3. Commit and push to main branch
4. GitHub Pages will automatically redeploy

### Custom Domain (Optional)
To use a custom domain (e.g., portfolionecromancer.com):

1. In **Settings** → **Pages**
2. Under **Custom domain**, enter your domain
3. Add DNS records as instructed
4. Wait for DNS propagation (up to 24 hours)

## Integration Documentation

The `INTEGRATIONS.md` file provides detailed setup instructions for all integrations:

### Available Integrations
1. **Google APIs** (Gmail, Drive, Docs)
   - Email and file scraping
   - OAuth setup guide
   
2. **Slack**
   - Team conversation scraping
   - Bot token setup
   
3. **Figma**
   - Design file access
   - Personal token setup
   
4. **OpenAI**
   - AI categorization and summaries
   - API key configuration
   
5. **Local Screenshots**
   - File system scanning
   - No API needed

All integrations are optional and fully documented.

## Troubleshooting

### GitHub Pages Not Showing
- **Check**: Settings → Pages shows green "Your site is published" message
- **Wait**: Allow 1-3 minutes for first deployment
- **Verify**: Branch is set to `main` and folder to `/docs`
- **Clear cache**: Try opening in incognito/private window

### 404 Error
- **Check**: Files exist in `docs/` directory on main branch
- **Verify**: `index.html` exists at `docs/index.html`
- **Wait**: Can take a few minutes after pushing changes

### Styling Issues
- **Check**: `style.css` is in the same directory as `index.html`
- **Verify**: Link in HTML: `<link rel="stylesheet" href="style.css">`
- **Clear cache**: Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)

## Next Steps

1. ✅ Enable GitHub Pages (follow Step 1 above)
2. ✅ Verify the landing page loads correctly
3. ✅ Share the URL with potential users
4. ✅ Consider adding custom domain
5. ✅ Update content as project evolves

## Support

- **Documentation**: See `docs/README.md` for local development
- **Integrations**: See `INTEGRATIONS.md` for API setup
- **Project Docs**: See main `README.md` for usage
- **Issues**: Open on GitHub for bugs or questions

---

**Your landing page is ready to go live!** Just follow Step 1 above to enable GitHub Pages.
