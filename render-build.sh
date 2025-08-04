#!/usr/bin/env bash
# Install Chrome & Chromedriver for Render

apt-get update
apt-get install -y wget unzip curl gnupg

# Install Google Chrome
curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb
apt install -y ./chrome.deb

# Confirm versions
google-chrome --version
