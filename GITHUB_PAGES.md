# GitHub Pages Deployment Guide

## 🚀 SIG Consulting - GitHub Pages Setup

Your Quarto website is now configured for GitHub Pages deployment! Here are the setup steps and deployment options.

## 📋 What Was Configured

### ✅ **_quarto.yml Updates**
- Added `output-dir: docs` to build to the right folder
- Added `site-url` and `repo-url` for proper GitHub Pages integration
- Added `repo-actions` for edit/issue links
- Added footer with GitHub links

### ✅ **GitHub Actions Workflow**
- Created `.github/workflows/deploy-pages.yml`
- Automated deployment on every push to main
- Handles Python dependencies with UV
- Uses sample data for public deployment

### ✅ **Build Scripts**
- `build-pages.sh` for local testing
- Proper environment handling
- Error checking and validation

## 🎯 Deployment Options

### Option 1: Automatic Deployment (Recommended)

1. **Push your code** to GitHub:
   ```bash
   git add .
   git commit -m "Configure for GitHub Pages deployment"
   git push origin main
   ```

2. **Enable GitHub Actions** in your repository:
   - Go to GitHub Settings > Pages
   - Select "GitHub Actions" as source
   - The workflow will run automatically

3. **Your site will be live at**: `https://softloud.github.io/sig-consulting`

### Option 2: Manual Deployment

1. **Build locally**:
   ```bash
   ./build-pages.sh
   ```

2. **Push the docs folder**:
   ```bash
   git add docs/
   git commit -m "Build site for GitHub Pages"
   git push origin main
   ```

3. **Configure GitHub Pages**:
   - Go to Settings > Pages
   - Select "Deploy from a branch"
   - Choose "main" branch and "/docs" folder

## 🔧 Local Development

### Preview Changes Locally
```bash
# Start development server
quarto preview

# Or use the dev server script
./dev-server.sh
```

### Test GitHub Pages Build
```bash
# Test the exact build process
./build-pages.sh

# Check the built site
cd docs && python -m http.server 8000
# Visit: http://localhost:8000
```

## 🔒 Security Considerations

### ✅ **Safe for Public Deployment**
- All credentials are removed from output
- Uses sample data for public demos
- Environment variables are safely handled
- No sensitive URLs or keys exposed

### 🔧 **Data Source Configuration**
- **Local development**: Uses your real Google Sheets data
- **Public deployment**: Uses sample data (`local-data/sample-google-template.csv`)
- **GitHub Actions**: Automatically creates safe environment

## 📊 Site Structure

```
https://softloud.github.io/sig-consulting/
├── index.html              # Landing page
├── sig.html                # Main analysis dashboard  
├── SIGVIS_GUIDE.html        # Usage documentation
├── SIG_ARCHITECTURE.html    # Technical architecture
├── ROLE_SHAPES_GUIDE.html   # Role visualization guide
└── ...                     # Other documentation
```

## 🚨 Troubleshooting

### Build Fails
- Check that all dependencies are in `pyproject.toml`
- Ensure environment file is created correctly
- Verify Quarto can find Python dependencies

### Site Not Updating
- Check GitHub Actions logs in the "Actions" tab
- Ensure Pages is enabled in repository settings
- Verify the workflow has proper permissions

### Python Errors
- Ensure UV is properly handling dependencies
- Check that the sample data file exists
- Verify import paths are correct

## 🎉 Next Steps

1. **Customize your site** by editing the Quarto files
2. **Add your real data** for private development
3. **Share the public URL** with your team
4. **Set up custom domain** (optional) in GitHub Pages settings

Your SIG Consulting website is ready for the world! 🌐