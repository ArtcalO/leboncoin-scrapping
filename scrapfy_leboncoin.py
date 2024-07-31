KEY = "scp-live-55facd3dd42d46fc9c77618cb7bb8eb9"

from scrapfly import ScrapeConfig, ScrapflyClient, ScrapeApiResponse
from typing import Dict, List
import asyncio
import json
import sys
import requests


def post_data(data):
    url = "https://api.example.com/users"
    headers = {'Content-Type': 'application/json'}
    data = {
      "name": "John Doe",
      "email": "johndoe@example.com",
      "password": "password123"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
      print("User created successfully")
    else:
      print("Error creating user:", response.text)

def get_object_by_value(data, key, value):
    for item in data:
        if item[key] == value:
            return item
    return None

SCRAPFLY = ScrapflyClient(key=KEY)

# scrapfly config
BASE_CONFIG = {
    # bypass web scraping blocking
    "asp": True,
    # set the proxy location to France
    "country": "fr",
}

def parse_search(result: ScrapeApiResponse):
    """parse search result data from nextjs cache"""
    # select the __NEXT_DATA__ script from the HTML
    next_data = result.selector.css("script[id='__NEXT_DATA__']::text").get()
    # extract ads listing data from the search page
    ads_data = json.loads(next_data)
    return ads_data['props']['pageProps']['ad']

async def scrape_search(url: str, max_pages: int) -> List[Dict]:
    """scrape leboncoin search"""
    print(f"scraping search {url}")
    first_page = await SCRAPFLY.async_scrape(ScrapeConfig(url, **BASE_CONFIG))
    search_data = parse_search(first_page)
    response = {
        'adresse':search_data["location"]["city_label"],
        'title': search_data["subject"],
        'prix':search_data["price_cents"]/100,
        'type_habitat':get_object_by_value(search_data["attributes"],"key","real_estate_type")['value_label'],
        'surface_habitable':get_object_by_value(search_data["attributes"],"key","square")['value_label'],
        'nbr_pieces':get_object_by_value(search_data["attributes"],"key","rooms")['value_label'],
        'description': search_data["body"]
        
    }
    
    return response

# run the scraping function

if __name__ == "__main__":
    url = sys.arg[1]
    response = asyncio.run(scrape_search(url=url, max_pages=1))

