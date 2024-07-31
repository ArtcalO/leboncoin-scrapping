from bs4 import BeautifulSoup
import requests

url = 'https://www.targetwebsite.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

for link in soup.select('a'):
    if 'display' in link.get('style', '') and 'none' in link['style']:
        continue  # Skip this link
    # Process link


import requests
from bs4 import BeautifulSoup

def detect_honeypots(url):
    # Fetch website content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Check for unusual URLs
    for link in soup.find_all('a'):
        href = link.get('href')
        if not href:
            continue

        if href.startswith('javascript:') or href.startswith('#'):
            continue

        if re.search(r'[_\d]+', href):  # Check for excessive underscores or numbers
            print(f"Suspicious URL: {href}")

    # Check for hidden fields with unusual names
    for form in soup.find_all('form'):
        for input in form.find_all('input', type='hidden'):
            name = input.get('name')
            if not name:
                continue

            if re.search(r'^[^a-zA-Z]*$', name):  # Check for non-alphanumeric characters
                print(f"Suspicious hidden field: {name}")

    # Check for excessive JavaScript
    script_count = len(soup.find_all('script'))
    if script_count > 50:  # Arbitrary threshold for excessive JavaScript
        print(f"Excessive JavaScript detected")

# Example usage
url = "https://example.com"
detect_honeypots(url)