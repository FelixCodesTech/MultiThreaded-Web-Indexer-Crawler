import requests
from bs4 import BeautifulSoup
import csv
import time
import threading

# Starting website
start_url = 'https://wordpress.com/'
count = 0
maxTimeout = 0.2

# Define a function to extract all links from a webpage
def extract_links(url):
    try:
        response = requests.get(url, timeout=maxTimeout)
        soup = BeautifulSoup(response.text, 'html.parser')
        base_url = response.url
        links = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and not (href.startswith('javascript:') or href.startswith('mailto:')):
                if href.startswith(('http', 'https')):
                    href = href.strip('\'"')
                    links.append(href)
                elif href.startswith('/'):
                    continue
                    #href = base_url + href
                    #links.append(href)
        return links
    except Exception:
        global count
        count += 1

# Check if a link is already in the CSV file
def is_duplicate(url):
    with open('sites.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == url:
                return True
    return False

# Function to crawl a website and save its links to the CSV file
def crawl_website(url):
    try:
        global count
        print(f"Current Round: {count}, having {int(threading.active_count())} agents")
        links = extract_links(url)
        with open('sites.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for link in links:
                if not is_duplicate(link):
                    writer.writerow([link])
        count += 1
    except Exception:
        count += 1

# Save links from the starting website to a CSV file
links = extract_links(start_url)
with open('sites.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for link in links:
        if not is_duplicate(link):
            writer.writerow([link])

# Crawl through all websites listed in the CSV file using multi-threading
while True:
    try:
        with open('sites.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            urls = [row[0] for row in reader]
            threads = []
            for url in urls[count:]:
                if threading.active_count() < 100000000: # limit the number of threads to 10
                    t = threading.Thread(target=crawl_website, args=(url,))
                    threads.append(t)
                    t.start()
        for t in threads:
            t.join()
        # Save the CSV file every 10 minutes
        #time.sleep(600)
    except Exception:
        print(f"Error, trying again")
        count += 1