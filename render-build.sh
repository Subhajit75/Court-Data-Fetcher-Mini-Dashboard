#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies for Chrome
echo "Installing Chromium dependencies..."
apt-get update
apt-get install -y wget unzip fontconfig locales gconf-service libx11-6 libx11-xcb1 libxcb1 libxcomposite1 \
libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 libc6 \
libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libglib2.0-0 libgtk-3-0 \
libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-xcb1 zlib1g lsb-release xdg-utils

# Download latest stable Chromium for Linux
echo "Downloading latest Chromium..."
mkdir -p .chromium
cd .chromium
wget https://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_x64/1120000/chrome-linux.zip
unzip chrome-linux.zip
mv chrome-linux chrome
cd ..

# Set Chrome binary path for Render
echo "GOOGLE_CHROME_BIN=$PWD/.chromium/chrome/chrome" >> $GITHUB_ENV

# Install Python requirements
pip install --upgrade pip



# Confirm versions
google-chrome --version
