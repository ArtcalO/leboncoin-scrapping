# with open("valid_proxies.txt", "r") as f:
#     proxies = f.read().split("\n")
import requests

def check_proxy(proxy):
  try:
    response = requests.get('http://httpbin.org/ip', proxies={'http': proxy, 'https': proxy}, timeout=5)
    print(response.json())
    if response.status_code == 200 and response.json()['origin'] != proxy.split(':')[0]:
      return True  
    else:
      return False
  except requests.exceptions.RequestException:
    return False


#for proxy in proxies:
if check_proxy("13.83.94.137:3128"):
  print('Proxy is working')
else:
  print('Proxy is not working')