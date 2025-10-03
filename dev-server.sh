#!/bin/bash

# Development server script for SIG Consulting
# This script sets up the development environment and starts the Quarto preview server

echo "🚀 Starting SIG Consulting Development Server..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ UV is not installed. Please install it first:"
    echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Check if .env file exists
if [ ! -f "client_credentials/.env" ]; then
    echo "⚠️  Environment file not found. Creating from template..."
    cp templates/.env-template client_credentials/.env
    echo "📝 Please update client_credentials/.env with your configuration"
fi

# Install dependencies
echo "📦 Installing dependencies..."
uv sync

# Start Quarto preview
echo "🌐 Starting Quarto preview server..."
echo "📱 The site will be available at: http://localhost:4200"
echo "🔄 Auto-reload is enabled - changes will be reflected automatically"
echo "⏹️  Press Ctrl+C to stop the server"

quarto preview --port 4200