import json
import yaml
from bs4 import BeautifulSoup
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, 'config', 'scraper_config.yaml')
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')

def load_config():
    with open(CONFIG_PATH, 'r') as file:
        return yaml.safe_load(file)

def setup_driver():
    """Sets up the Selenium WebDriver."""
    try:
        print("Setting up Selenium WebDriver...")
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        print("WebDriver setup complete.")
        return driver
    except WebDriverException as e:
        print(f"Error setting up WebDriver: {e}")
        print("Please ensure you have Google Chrome and the correct chromedriver installed.")
        return None

def get_page_content(driver, url):
    """Gets page content using Selenium."""
    try:
        driver.get(url)
        
        # Handle cookie consent banner
        try:
            wait = WebDriverWait(driver, 10)
            accept_button = wait.until(EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button")))
            accept_button.click()
            print("Clicked the cookie consent button.")
            time.sleep(3)
        except TimeoutException:
            print("Cookie consent banner not found or already handled.")
            pass

        # Scroll down to trigger dynamic loading
        print("Scrolling down to load products...")
        scroll_pause_time = 2
        scrolls = 3
        for i in range(scrolls):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            print(f"Scroll {i+1}/{scrolls}...")

        # Now, wait for the product cards to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="product-card"]'))
        )
        return BeautifulSoup(driver.page_source, 'html.parser')
    except TimeoutException:
        print("Timed out waiting for product cards to appear. The page might be empty or the selector is wrong.")
        return None
    except WebDriverException as e:
        print(f"Error fetching {url} with Selenium: {e}")
        return None

def parse_product(product_card, category_name, base_url):
    """
    Parses a single product card from the category page for ManoMano.
    """
    data = {
        'product_name': None,
        'category': category_name,
        'price': None,
        'currency': 'EUR',
        'product_url': None,
        'brand': None,
        'measurement_unit': None, # Not available on card
        'photo_url': None,
    }

    # The whole card is a link
    link_tag = product_card.find('a')
    if not link_tag:
        return None # Can't get URL or name without this

    # Product URL
    href = link_tag.get('href')
    if href:
        data['product_url'] = base_url + href if href.startswith('/') else href

    # Product Name
    # The name is just text inside the link, not in a specific tag
    name_element = link_tag.find('p') # Heuristic, might need adjustment
    if name_element:
         data['product_name'] = name_element.get_text(strip=True)

    # Price
    price_tag = product_card.find('div', {'data-testid': 'product-price'})
    if price_tag:
        price_text = price_tag.get_text(strip=True).replace('€', '').replace(',', '.').strip()
        try:
            data['price'] = float(price_text)
        except (ValueError, TypeError):
            data['price'] = None

    # Brand
    brand_tag = product_card.find('p', {'data-testid': 'product-brand'})
    if brand_tag:
        data['brand'] = brand_tag.get_text(strip=True)

    # Photo URL
    img_tag = product_card.find('img')
    if img_tag and img_tag.has_attr('src'):
        data['photo_url'] = img_tag['src']
        
    if data['product_name'] and data['price'] and data['product_url']:
        return data
    return None


def scrape_category(driver, category, base_url, max_products_per_category=25):
    products = []
    page_num = 1
    while len(products) < max_products_per_category:
        paginated_url = f"{base_url}{category['path']}?page={page_num}"
        print(f"Scraping {paginated_url} for category {category['name']}...")
        
        soup = get_page_content(driver, paginated_url)
        
        if not soup:
            break

        product_cards = soup.select('div[data-testid="product-card"]')
        if not product_cards:
            print(f"No more product cards found for {category['name']} on page {page_num}.")
            break

        for card in product_cards:
            product_data = parse_product(card, category['name'], base_url)
            if product_data:
                products.append(product_data)
                if len(products) >= max_products_per_category:
                    break
        
        page_num += 1

    return products

def main():
    driver = setup_driver()
    if not driver:
        return

    try:
        config = load_config()
        base_url = config['base_url']
        all_products = []
        
        total_product_goal = 100
        products_per_category = total_product_goal // len(config['categories']) + 1

        for category in config['categories']:
            products_scraped = scrape_category(driver, category, base_url, max_products_per_category=products_per_category)
            all_products.extend(products_scraped)

        # Save data
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(os.path.join(DATA_DIR, 'materials.json'), 'w', encoding='utf-8') as f:
            json.dump(all_products, f, indent=4, ensure_ascii=False)

        print(f"\nScraping complete. Total products scraped: {len(all_products)}")
        print(f"Data saved to data/materials.json")
    finally:
        if driver:
            print("Closing WebDriver.")
            driver.quit()

if __name__ == "__main__":
    main()
