import requests
import json
import yaml
import os
import re
import logging
import sys

from bs4 import BeautifulSoup as bs
from pydantic import BaseModel
from typing import Optional

URL = "https://www.lego.com/pl-pl/product/captain-jack-sparrows-pirate-ship-10365"
SYSTEM_CA_BUNDLE = '/etc/ssl/certs/ca-certificates.crt'

APP_TOKEN = os.environ.get("LEGO_APP_TOKEN")
USER_TOKEN = os.environ.get("LEGO_USER_TOKEN")
PUSHOVER_URL = os.environ.get("PUSHOVER_URL")

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}

REGEX = r"\b(\d{1,2})\s+(stycznia|lutego|marca|kwietnia|maja|czerwca|lipca|sierpnia|września|października|listopada|grudnia)\s+(\d{4})\b"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)

logger = logging.getLogger(__name__)

class LegoData(BaseModel):
    price: Optional[str] = "N/A"
    availability: Optional[str] = "N/A"
    
    def format_pushover_message(self) -> str:
        return f'Cena: {self.price}, Wysyłka: {self.availability}'


def get_data_from_web() -> LegoData:
    
    """
    Return data from LEGO page regarding price and availability.
    
    """
    
    data_dict = {
        'price': 'N/A',
        'availability': 'N/A'
    }
    
    logger.info("Starting data retriving from LEGO website.")
    
    try:
        response = requests.get(URL, headers=HEADERS, verify=SYSTEM_CA_BUNDLE)
        response.raise_for_status()
        logger.info("Succesfully scraped the website. Status 200.")
    except requests.exceptions.RequestException as e:
        logger.error("Connection error: {e}", exc_info=True)
        raise e

    soup = bs(response.text, 'html.parser')

    price_element = soup.select_one('span[data-test="product-price-display-price"]')
    if price_element:
        data_dict['price'] = price_element.get_text(strip=True)
        logger.info("Price captured!")
        
    availability_element = soup.select_one('span[data-test="product-overview-availability"]')
    regex_availability = availability_element.get_text(strip=True)
    match = re.search(REGEX, regex_availability).group()
    if match:
        data_dict['availability'] = match
        logger.info("Availability captured!")
    
    return LegoData(**data_dict)

def pushover_handler(lego_data: LegoData):

    payload = {
        "token": APP_TOKEN,
        'user': USER_TOKEN,
        "message": lego_data.format_pushover_message(),
        "title": 'Lego Jack\'s Ship Status',
        "sound": "bike"
    }

    try:
        response = requests.post(PUSHOVER_URL, data = payload, timeout=5)
        response.raise_for_status()
        logger.info("Message successfully pushed.")
    except requests.exceptions.RequestException as e:
        logger.error("Connection error: {e}", exc_info=True)

if __name__ == "__main__":
    data = get_data_from_web()
    pushover_handler(data)