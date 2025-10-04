from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service

URL = "https://www.lego.com/pl-pl/product/captain-jack-sparrows-pirate-ship-10365"

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage') 
options.add_argument('--disable-gpu')
DRIVER_PATH ='/usr/bin/chromedriver'
service = Service(DRIVER_PATH)

try:
    driver = webdriver.Chrome(service=service, options=options)
except Exception as e:
    print(f"Error during initialization. Details: {e}")
    exit()

wait = WebDriverWait(driver, 20)

print(f"Forwarding to page: {URL}")

driver.get(URL)

price_group = wait.until(
    EC.presence_of_element_located
    ((By.CSS_SELECTOR, 'span[data-test="product-price-display-price"]')))

price = price_group.text.strip()

availability_group = wait.until(
    EC.presence_of_element_located
    ((By.CSS_SELECTOR, 'span[data-test="product-overview-availability"]')))

availability = availability_group.text.strip().split('się')[1]

print(price, availability)