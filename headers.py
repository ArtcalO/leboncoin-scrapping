url = 'https://www.targetwebsite.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'Referer': 'https://www.google.com/',
    'Accept-Language': "",
    'Accept-Encoding': "",
    'Connection': ""
}

response = requests.get(url, headers=headers)



from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent # pip3 install fake_useragent
from time import sleep

options = Options()
options.add_argument(f'user-agent={UserAgent().random}')
driver = webdriver.Chrome(chrome_options=options)
driver.get("http://www.whatsmyua.info/")

sleep(5)

driver.execute_cdp_cmd("Network.enable", {})
driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": f"{UserAgent().random}"}})
driver.get("http://www.whatsmyua.info/")