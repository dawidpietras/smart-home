import requests
import json
import yaml
import os

from bs4 import BeautifulSoup as bs

URL = "https://www.lego.com/pl-pl/product/captain-jack-sparrows-pirate-ship-10365"
SYSTEM_CA_BUNDLE = '/etc/ssl/certs/ca-certificates.crt'

APP_TOKEN = os.environ.get("LEGO_APP_TOKEN", 'axqb5973zrcu3ed7bmya8e13izhx6z')
USER_TOKEN = os.environ.get("LEGO_USER_TOKEN", 'u65vsygubbicdo7uskjj477zvh1ah9')
PUSHOVER_URL = os.environ.get("PUSHOVER_URL", "https://api.pushover.net/1/messages.json")

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}


def get_data_from_web():
    
    """
        Return data from LEGO page regarding price and availability.
    """
    
    response = requests.get(URL, headers=headers, verify=SYSTEM_CA_BUNDLE)
    response.raise_for_status()

    soup = bs(response.text, 'html.parser')

    price_element = soup.select_one('span[data-test="product-price-display-price"]')
    if price_element:
        price = price_element.get_text(strip=True)
        print(f"Cena: {price}")
    else:
        print("Cena: Element nie został znaleziony w statycznym HTML.")
        
    availability_element = soup.select_one('span[data-test="product-overview-availability"]')

    if availability_element:
        availability = availability_element.get_text(strip=True).split('się')[1]
        print(f"Dostępność: {availability}")
    else:
        print("Dostępność: Element nie został znaleziony w statycznym HTML.")

def pushover_handler()

payload = {
    "token": APP_TOKEN,
    'user': USER_TOKEN,
    "message": None,
    "title": 'Lego Jack\'s Ship Status',
    "sound": "bike"
}

payload['message'] = f'{price} {availability}'

response = requests.post(PUSHOVER_URL, data = payload)

print(response.status_code)
