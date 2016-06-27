from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os

# https://sites.google.com/a/chromium.org/chromedriver/downloads
# Go to the link above and download the driver for your system
# Then write the path to that file (once it has been unzipped)
chromeDriver = r'path\to\chromedriver.exe'

chrome = webdriver.Chrome(executable_path=chromeDriver)

chrome.get('https://www.whatever_website.com')
