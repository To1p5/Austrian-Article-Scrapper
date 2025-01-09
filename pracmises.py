from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import time
import random
import os
from Am import create_audio
import re

# Scrapper for mises.org
def extract_article(url):
    chrome_options = Options()
    ua = UserAgent()
    chrome_options.add_argument(f'user-agent={ua.random}')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(url)
        time.sleep(random.uniform(2, 5))
        
        title = driver.find_elements(By.CSS_SELECTOR, "By.CSS_SELECTOR, a.text-misesBlue")
        
        # Remove quotes from the title
        title = title.replace("'", "").replace('"', "")
        
        
        
        return title,
    
    finally:
        driver.quit()

def save_to_file(title, content, url):
    filename = ''.join(e for e in title if e.isalnum() or e.isspace())
    filename = filename.replace(' ', '_') + '.txt'
    
    if len(filename) > 255:
        filename = filename[:255]
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"URL: {url}\n\n")
        f.write(f"Title: {title}\n\n")
        f.write("Content:\n\n")
        f.write(content)
    
    return filename

# Usage
url = "https://mises.org/wire"
title, content = extract_article(url)

# Save the extracted information to a file
filename = save_to_file(title, content, url)

print(f"Article information has been saved to {os.path.abspath(filename)}")

# Create audio file
audio_filename = create_audio(filename, title)
print(f"Audio version has been saved as {os.path.abspath(audio_filename)}")



