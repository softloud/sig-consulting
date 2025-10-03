#!/bin/bash

# GitHub Pages Deployment Script for SIG Consulting
# This script builds the site locally for testing before deployment

echo "🚀 Building SIG Consulting site for GitHub Pages..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ UV is not installed. Please install it first:"
    echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Check if quarto is installed
if ! command -v quarto &> /dev/null; then
    echo "❌ Quarto is not installed. Please install it first:"
    echo "Visit: https://quarto.org/docs/get-started/"
    exit 1
fi

# Check if .env file exists
if [ ! -f "client_credentials/.env" ]; then
    echo "⚠️  Environment file not found. Creating minimal version for build..."
    echo "DATA_ENTRY=local-data/sample-google-template.csv" > client_credentials/.env
fi

# Install dependencies
echo "📦 Installing dependencies..."
uv sync

# Clean previous build
echo "🧹 Cleaning previous build..."
rm -rf docs

# Build the site
echo "🔨 Building Quarto website..."
uv run quarto render

# Check if build was successful
if [ -d "docs" ] && [ -f "docs/index.html" ]; then
    echo "✅ Build successful!"
    echo "📁 Site built in 'docs' folder"
    echo "🌐 Preview locally: quarto preview"
    echo ""
    echo "📋 Next steps for GitHub Pages:"
    echo "1. Commit and push your changes"
    echo "2. Go to GitHub > Settings > Pages"
    echo "3. Set source to 'Deploy from a branch'"
    echo "4. Select 'main' branch and '/docs' folder"
    echo "5. Your site will be available at: https://softloud.github.io/sig-consulting"
else
    echo "❌ Build failed!"
    exit 1
fi