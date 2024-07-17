import time
import random

urls = ['https://www.targetwebsite.com/page1', 'https://www.targetwebsite.com/page2', 'https://www.targetwebsite.com/page3']

for url in urls:
    response = requests.get(url)
    # Process response
    sleep_time = random.uniform(1, 10)  # Generate a random sleep time between 1 and 10 seconds
    time.sleep(sleep_time)  # Sleep for a random time between requests