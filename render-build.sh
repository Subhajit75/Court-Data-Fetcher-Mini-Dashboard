#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install required Linux packages
apt-get update
apt-get install -y wget unzip gnupg curl \
    libx11-6 libxcomposite1 libxcursor1 \
    libxdamage1 libxext6 libxi6 libxrender1 \
    libxss1 libxtst6 libnss3 libglib2.0-0 libgconf-2-4 \
    libxrandr2 libasound2 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libdbus-1-3 libxshmfence1 libgbm1 \
    fonts-liberation libappindicator3-1 libxkbcommon0

# Download Chromium
wget https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.86/linux64/chrome-linux64.zip
unzip chrome-linux64.zip
mv chrome-linux64 /usr/local/chrome

# Export Chrome path for Render
export GOOGLE_CHROME_BIN=/usr/local/chrome/chrome

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
