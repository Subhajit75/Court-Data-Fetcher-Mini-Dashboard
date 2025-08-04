#!/usr/bin/env bash
set -o errexit

echo "Downloading portable Chromium..."
mkdir -p .chromium
cd .chromium
wget https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.86/linux64/chrome-linux64.zip
unzip chrome-linux64.zip
mv chrome-linux64 chrome
cd ..

echo "GOOGLE_CHROME_BIN=$PWD/.chromium/chrome/chrome" >> $GITHUB_ENV

pip install --upgrade pip
