#!/usr/bin/env bash
# Install Chrome and ChromeDriver in Render for Selenium

echo "---- Installing Google Chrome ----"
apt-get update
apt-get install -y wget unzip curl

# Install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get install -y ./google-chrome-stable_current_amd64.deb

# Install ChromeDriver (latest)
CHROME_VERSION=$(google-chrome --version | sed 's/Google Chrome //g' | cut -d '.' -f 1)
DRIVER_VERSION=$(curl -sS "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
wget -N "https://chromedriver.storage.googleapis.com/${DRIVER_VERSION}/chromedriver_linux64.zip" -P ~/
unzip ~/chromedriver_linux64.zip -d ~/
mv -f ~/chromedriver /usr/local/bin/chromedriver
chmod 0755 /usr/local/bin/chromedriver

echo "---- Chrome and ChromeDriver installed ----"
