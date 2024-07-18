from bs4 import BeautifulSoup
import requests

url = 'https://www.targetwebsite.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

for link in soup.select('a'):
    if 'display' in link.get('style', '') and 'none' in link['style']:
        continue  # Skip this link
    # Process link