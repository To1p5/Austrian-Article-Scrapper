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
        # Convert "MM/DD/YYYY" format to datetime
        return datetime.strptime(date_string.strip(), "%m/%d/%Y")
    except ValueError as e:
        print(f"Error parsing date: {date_string}")
        return None

def get_mises_articles():
    chrome_options = Options()
    ua = UserAgent()
    chrome_options.add_argument(f'user-agent={ua.random}')
    chrome_options.add_argument('--log-level=3')  # Reduce logging
    
    driver = webdriver.Chrome(options=chrome_options)
    articles = []
    current_page = 1
    two_months_ago = datetime.now() - timedelta(days=60)
    reached_old_articles = False
    
    try:
        while not reached_old_articles:
            url = f"https://mises.org/wire?page={current_page}"
            driver.get(url)
            time.sleep(random.uniform(2, 4))
            
            # Wait for articles to be present
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "mises-link"))
            )
            
            # Get all article containers
            article_containers = driver.find_elements(By.CLASS_NAME, "mises-link")
            
            if not article_containers:
                print(f"No articles found on page {current_page}")
                break
                
            print(f"Found {len(article_containers)} articles on page {current_page}")
            
            # Process each article
            for container in article_containers:
                try:
                    # Get the title from the link inside the h3
                    title = container.find_element(By.CSS_SELECTOR, "a[data-component-id='mises:atom-link']").text.strip()
                    
                    # Find the parent article container and then the time element
                    article_div = container.find_element(By.XPATH, "../..")  # Go up to the article container
                    date_elem = article_div.find_element(By.TAG_NAME, "time")
                    date_text = date_elem.text.strip()
                    
                    print(f"Processing article: {title} ({date_text})")
                    
                    article_date = parse_date(date_text)
                    if not article_date:
                        continue
                    
                    if article_date < two_months_ago:
                        print(f"Found article older than 2 months: {date_text}")
                        reached_old_articles = True
                        break
                    
                    articles.append({
                        'title': title,
                        'date': article_date.strftime("%Y-%m-%d")
                    })
                    
                except Exception as e:
                    print(f"Error processing article: {str(e)}")
                    continue
            
            if reached_old_articles:
                break
                
            try:
                # Look for the next page link
                next_button = driver.find_element(By.CSS_SELECTOR, "li.pager__item--next a")
                if not next_button.is_displayed():
                    print("Next button not visible")
                    break
                    
                # Scroll the next button into view
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                time.sleep(1)
                
                next_button.click()
                print(f"Moving to page {current_page + 1}")
                current_page += 1
                time.sleep(2)  # Wait for page to load
            except Exception as e:
                print(f"No next page found: {str(e)}")
                break
                
    finally:
        driver.quit()
    
    return articles

if __name__ == "__main__":
    current_date = datetime.now()
    two_months_ago = current_date - timedelta(days=60)
    print(f"Collecting articles from {current_date.strftime('%B %d, %Y')} to {two_months_ago.strftime('%B %d, %Y')}")
    
    articles = get_mises_articles()
    
    # Sort articles by date (newest first)
    articles.sort(key=lambda x: x['date'], reverse=True)
    
    # Save results to a file
    with open("mises_recent_articles.txt", "w", encoding="utf-8") as f:
        f.write(f"Mises.org Articles from the Last 60 Days (as of {current_date.strftime('%B %d, %Y')})\n")
        f.write(f"Date Range: {current_date.strftime('%B %d, %Y')} to {two_months_ago.strftime('%B %d, %Y')}\n")
        f.write("=" * 80 + "\n\n")
        
        for article in articles:
            f.write(f"{article['date']} - {article['title']}\n")
    
    print(f"Found {len(articles)} articles from the last 60 days")
    print("Results have been saved to mises_recent_articles.txt") 