KEY = "YOUR-KEY-HERE"

from scrapfly import ScrapeConfig, ScrapflyClient, ScrapeApiResponse
from typing import Dict, List
import asyncio
import json
import sys
import requests


def post_data(incoming_data):
    url = "https://ibisokozo.ksquad.dev/rest_api/leboncoin-scrapped-items/"
    headers = {'Content-Type': 'application/json'}
    data = incoming_data
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
      print("Data posted")
    else:
      print("Error while posting data", response.text)

def get_object_by_value(data, key, value):
    for item in data:
        if item[key] == value:
            return item
    return None

SCRAPFLY = ScrapflyClient(key=KEY)

BASE_CONFIG = {
    "asp": True,
    "country": "fr",
}

def parse_search(result: ScrapeApiResponse):
    next_data = result.selector.css("script[id='__NEXT_DATA__']::text").get()
    ads_data = json.loads(next_data)
    return ads_data['props']['pageProps']['ad']

async def scrape_search(url: str, max_pages: int) -> List[Dict]:
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


import time

if __name__ == "__main__":
    start_time = time.time()

    url = sys.argv[1]
    response = asyncio.run(scrape_search(url=url, max_pages=1))
    post_data(response)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Elapsed time:", elapsed_time, "seconds")

