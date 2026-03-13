#!/bin/bash
# Build script for Audio Clip Extractor macOS app bundle.
#
# Prerequisites:
#   - Python 3.9+
#   - pip install pyinstaller
#   - FFmpeg installed (brew install ffmpeg)
#
# Usage:
#   cd audio_extractor
#   bash packaging/build.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=== Audio Clip Extractor — macOS Build ==="
echo "Project root: $PROJECT_ROOT"
echo ""

# Check Python
python3 --version || { echo "Python 3 not found"; exit 1; }

# Install build dependencies
echo "Installing build dependencies..."
pip3 install pyinstaller --quiet

# Install project dependencies
echo "Installing project dependencies..."
pip3 install -r "$PROJECT_ROOT/requirements.txt" --quiet

# Run the build
echo "Running PyInstaller build..."
python3 "$SCRIPT_DIR/build_macos.py"

echo ""
echo "=== Build Complete ==="
echo "The app is at: $PROJECT_ROOT/dist/AudioClipExtractor.app"
echo "To test: open $PROJECT_ROOT/dist/AudioClipExtractor.app"
