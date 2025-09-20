#!/bin/bash

# Simple build script for nest-cli

set -e

echo "🏗️  Building nest-cli for Linux..."

# Check if we have PyInstaller
if ! command -v pyinstaller &> /dev/null; then
    echo "Installing PyInstaller..."
    pip install pyinstaller
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.spec

# Build with PyInstaller
echo "📦 Building binary..."
pyinstaller \
    --onefile \
    --name=nest-cli \
    --add-data="tools:tools" \
    --hidden-import=runtime_patch \
    --hidden-import=tools.nix.management \
    --hidden-import=tools.domains.management \
    --hidden-import=tools.databases.management \
    --hidden-import=tools.github.management \
    --hidden-import=tools.caddy.management \
    --hidden-import=ai \
    --hidden-import=utils \
    --hidden-import=colorama \
    --hidden-import=requests \
    --hidden-import=questionary \
    --hidden-import=psycopg2 \
    --hidden-import=cryptography \
    main.py

echo "✅ Build complete!"
echo "📍 Binary location: $(pwd)/dist/nest-cli"
echo ""
echo "🧪 Test the binary:"
echo "   ./dist/nest-cli"
echo ""
echo "📦 Install system-wide:"
echo "   sudo cp dist/nest-cli /usr/local/bin/"
echo ""
echo "🚀 Create portable package:"
echo "   tar -czf nest-cli-linux.tar.gz -C dist nest-cli"
