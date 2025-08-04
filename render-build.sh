#!/usr/bin/env bash
# Render Build Script for Selenium + Chromium (no apt-get)

echo "Downloading portable Chromium..."
mkdir -p .chromium
cd .chromium

# Download prebuilt Chromium snapshot (approx 130MB)
wget https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/1090000/chrome-linux.zip -O chrome-linux.zip
unzip chrome-linux.zip
mv chrome-linux chrome

# Export the Chrome binary path for runtime
echo "GOOGLE_CHROME_BIN=$(pwd)/chrome/chrome" >> $GITHUB_ENV


# Confirm versions
google-chrome --version
