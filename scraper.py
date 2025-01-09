from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import time
import random

def extract_article(url):
    # Set up Chrome options
    chrome_options = Options()
    ua = UserAgent()
    chrome_options.add_argument(f'user-agent={ua.random}')
    
    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Navigate to the website
        driver.get(url)
        
        # Add a random delay to simulate human behavior
        time.sleep(random.uniform(2, 5))
        
        # Extract the title
        title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        ).text
        
        # Extract the subtitle
        subtitle = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h2"))
        ).text
        
        # Extract the article content
        article_wrapper = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.article-wrapper.py-2.mt-5"))
        )
        paragraphs = article_wrapper.find_elements(By.TAG_NAME, "p")
        article_content = "\n\n".join([p.text for p in paragraphs])
        
        return title, subtitle, article_content
    
    finally:
        # Close the browser
        driver.quit()

# Usage
url = "https://fee.org/articles/our-cities-are-zoned-out/"
title, subtitle, content = extract_article(url)

print(f"Title: {title}")
print(f"Subtitle: {subtitle}")
print(f"Article content: {content[:500]}...")  # Print first 500 characters of content

