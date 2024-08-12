"""
Author: Carmel NIYUNGEKO [ArtcalO TLW]
Github: https//:github.com/ArtcalO
Email: niyca14@gmail.com, artcalo@ksquad.dev
Date: 2024-07-31
Description: This script does webscrapping of lebon coin

"""
#

#KEY = "YOUR-KEY-HERE"


from scrapfly import ScrapeConfig, ScrapflyClient, ScrapeApiResponse
from typing import Dict, List
import asyncio
import json
import sys
import requests
import time
import datetime

def fetch_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return None


def post_data(incoming_data):
    url = "https://scrapping.fenfly.co.bi/rest_api/scrapped-items/"
    #url = "http://127.0.0.1:8000/rest_api/scrapped-items/"
    headers = None #{'Content-Type': 'application/json'}
    data = incoming_data
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"image_{timestamp}.jpeg"
    files = {'file': (filename, incoming_data['image_1'], 'image/jpeg')}
    response = requests.post(url, files=files,data=data,headers=headers)

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
    while not "ad" in ads_data['props']['pageProps']:
        time.sleep(1)
    return ads_data['props']['pageProps']['ad']

async def scrape_search(url: str, max_pages: int):
    print(f"scraping search {url}")
    try:
        first_page = await asyncio.wait_for(SCRAPFLY.async_scrape(ScrapeConfig(url, **BASE_CONFIG)), timeout=10)
        search_data = parse_search(first_page)
        response = {
            'adresse':search_data["location"]["city_label"],
            'title': search_data["subject"],
            'prix':search_data["price_cents"]/100,
            'type_habitat':get_object_by_value(search_data["attributes"],"key","real_estate_type")['value_label'],
            'surface_habitable':get_object_by_value(search_data["attributes"],"key","square")['value_label'],
            'surface_terrain':get_object_by_value(search_data["attributes"],"key","land_plot_surface")['value_label'],
            'nbr_pieces':get_object_by_value(search_data["attributes"],"key","rooms")['value_label'],
            'dpe':get_object_by_value(search_data["attributes"],"key","energy_rate")['value_label'],
            'ges':get_object_by_value(search_data["attributes"],"key","ges")['value_label'],
            'description': search_data["body"],
            'images':{"urls":search_data['images']['urls']},
            'image_1':fetch_image(search_data['images']['urls'][0]),
            "html_content":first_page.content
            
        }
        
        return response
    except asyncio.TimeoutError:
        print("The scraping operation timed out.")
        return None

import time

if __name__ == "__main__":
    start_time = time.time()

    url = sys.argv[1]
    response = asyncio.run(scrape_search(url=url, max_pages=1))
    if response is not None:
        post_data(response)
    else:
        print("Scraping failed due to timeout.")
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Elapsed time:", elapsed_time, "seconds")

