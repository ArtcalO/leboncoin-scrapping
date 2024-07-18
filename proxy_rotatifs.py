import requests
from itertools import cycle

# List of proxies
proxy_list = ['ip1:port1', 'ip2:port2', ...]
proxy_pool = cycle(proxy_list) # create a cycle of proxies

url = 'https://www.targetwebsite.com'

for i in range(1,3):
    # Get a proxy from the pool
    proxy = next(proxy_pool)
    print(f"Request #{i}:")
    try:
        response = requests.get(url, proxies={"http": proxy, "https": proxy})
        print(response.content)
    except:
        # Most free proxies will often get connection errors, so we catch them here
        print("Connection error with proxy:", proxy)
