import requests
from bs4 import BeautifulSoup
import random
import concurrent.futures
import os
import time
from datetime import datetime, timedelta, date

ALL_PROXIES_NAME = "all_proxies.txt"
VALID_PROXIES_NAME = "valid_proxies.txt"

proxylist=None

def get_file_updated_at(file_path):
    modified_time = os.path.getmtime(file_path)
    return datetime.fromtimestamp(modified_time)

def check_proxies(p):
    try:
        res = requests.get("http://ipinfo.io/json", proxies={"http":p,"https":p}, timeout=3)
    except:
        return False
    if(res.status_code == 200):
        return True

def retriveProxiesFromFile():
    proxies=[]
    with open((ALL_PROXIES_NAME), "r", encoding='utf-8') as file:
        proxies = file.read().split("\n")
    for p in proxies:
        if(check_proxies(p)):
            with open((VALID_PROXIES_NAME), "a+", encoding='utf-8') as file2:
                print(f"{p}", file=file2)

def getProxies():
    r = requests.get('https://free-proxy-list.net/')
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('tbody')
    proxies = []
    for row in table:
        if row.find_all('td')[4].text =='elite proxy':
            proxy = ':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text])
            proxies.append(proxy)
            with open((ALL_PROXIES_NAME), "a+", encoding='utf-8') as file:
                print(f"{proxy}", file=file)
        else:
            pass

    retriveProxiesFromFile()

def check_proxies_file():
    today = datetime.now()
    all_proxies_file_path = os.path.join(os.getcwd(), ALL_PROXIES_NAME)
    valid_proxies_file_path = os.path.join(os.getcwd(), VALID_PROXIES_NAME)
    if os.path.exists(all_proxies_file_path):
        # verifier si le temps de modification du fichier depasse les 10 minutes
        # si oui on le supprime pour faire un update
        intervalle = (today-get_file_updated_at(all_proxies_file_path)) // timedelta(minutes=1)
        if(intervalle>10):
            os.remove(all_proxies_file_path)
            os.remove(valid_proxies_file_path)
            getProxies()
        else:
            retriveProxiesFromFile()
    else:
        getProxies()

check_proxies_file()

