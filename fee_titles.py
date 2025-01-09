from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from datetime import datetime, timedelta
import time
import random

def parse_date(date_string):
    try:
        # Convert "January 8, 2025" format to datetime
        return datetime.strptime(date_string.strip(), "%B %d, %Y")
    except ValueError as e:
        print(f"Error parsing date: {date_string}")
        return None

def get_fee_articles():
    chrome_options = Options()
    ua = UserAgent()
    chrome_options.add_argument(f'user-agent={ua.random}')
    chrome_options.add_argument('--log-level=3')  # Reduce logging
    
    driver = webdriver.Chrome(options=chrome_options)
    articles = []
    two_months_ago = datetime.now() - timedelta(days=60)
    processed_titles = set()  # Keep track of processed titles to avoid duplicates
    old_article_found = False
    last_height = 0
    
    try:
        driver.get("https://fee.org/archive")
        time.sleep(random.uniform(2, 4))
        
        while not old_article_found:
            # Get all article elements currently loaded (excluding author links)
            article_titles = driver.find_elements(By.CSS_SELECTOR, "p.featured-article-title a:not(.featured-article-author)")
            dates = driver.find_elements(By.CSS_SELECTOR, "span.featured-article-meta")
            
            # Process visible articles
            for title, date_elem in zip(article_titles, dates):
                title_text = title.text.strip()
                
                # Skip if we've already processed this title
                if title_text in processed_titles:
                    continue
                    
                # Parse the date
                article_date = parse_date(date_elem.text)
                if not article_date:
                    continue
                
                # If we find an article older than 2 months, stop processing
                if article_date < two_months_ago:
                    old_article_found = True
                    break
                
                processed_titles.add(title_text)
                articles.append({
                    'title': title_text,
                    'date': article_date.strftime("%Y-%m-%d")
                })
            
            if old_article_found:
                break
            
            # Store current height and scroll a smaller amount
            current_height = driver.execute_script("return window.pageYOffset;")
            # Scroll by 800 pixels (approximate viewport height)
            driver.execute_script("window.scrollBy(0, 800);")
            time.sleep(1.5)
            
            # Check if we've reached the bottom
            new_height = driver.execute_script("return window.pageYOffset;")
            if new_height == current_height:
                break
            
    finally:
        driver.quit()
    
    return articles

if __name__ == "__main__":
    current_date = datetime.now()
    two_months_ago = current_date - timedelta(days=60)
    print(f"Collecting articles from {current_date.strftime('%B %d, %Y')} to {two_months_ago.strftime('%B %d, %Y')}")
    
    articles = get_fee_articles()
    
    # Sort articles by date (newest first)
    articles.sort(key=lambda x: x['date'], reverse=True)
    
    # Save results to a file
    with open("fee_recent_articles.txt", "w", encoding="utf-8") as f:
        f.write(f"FEE.org Articles from the Last 60 Days (as of {current_date.strftime('%B %d, %Y')})\n")
        f.write(f"Date Range: {current_date.strftime('%B %d, %Y')} to {two_months_ago.strftime('%B %d, %Y')}\n")
        f.write("=" * 80 + "\n\n")
        
        for article in articles:
            f.write(f"{article['date']} - {article['title']}\n")
    
    print(f"Found {len(articles)} articles from the last 60 days")
    print("Results have been saved to fee_recent_articles.txt") 