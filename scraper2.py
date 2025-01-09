from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from Am import text_to_speech
import time
import random
import os

def extract_article(url):
    chrome_options = Options()
    ua = UserAgent()
    chrome_options.add_argument(f'user-agent={ua.random}')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(url)
        time.sleep(random.uniform(2, 5))
        
        title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        ).text
        
        subtitle = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h2"))
        ).text
        
        article_wrapper = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.article-wrapper.py-2.mt-5"))
        )
        paragraphs = article_wrapper.find_elements(By.TAG_NAME, "p")
        article_content = "\n\n".join([p.text for p in paragraphs])
        
        return title, subtitle, article_content
    
    finally:
        driver.quit()

def save_to_file(title, subtitle, content, url):
    filename = ''.join(e for e in title if e.isalnum() or e.isspace())
    filename = filename.replace(' ', '_') + '.txt'
    
    if len(filename) > 255:
        filename = filename[:255]
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"URL: {url}\n\n")
        f.write(f"Title: {title}\n\n")
        f.write(f"Subtitle: {subtitle}\n\n")
        f.write("Content:\n\n")
        f.write(content)
    
    return filename

# Usage
url = "https://fee.org/articles/homeschoolers-and-microschoolers-describe-the-benefits-of-alternative-education/"
title, subtitle, content = extract_article(url)

# Save the extracted information to a file
filename = save_to_file(title, subtitle, content, url)

# Create an audio filename based on the article title
audio_filename = ''.join(e for e in title if e.isalnum() or e.isspace())
audio_filename = audio_filename.replace(' ', '_')[:50] + '.mp3'  # Limit to 50 characters

# Convert the article content to speech
text_to_speech(content, audio_filename)

print(f"Article information has been saved to {os.path.abspath(filename)}")
print(f"Audio version has been saved as {os.path.abspath(audio_filename)}")
