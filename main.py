import requests
from bs4 import BeautifulSoup
import csv
import time

# Starting website
start_url = 'https://github.com/edoardottt/awesome-hacker-search-engines'
count = 0

# Define a function to extract all links from a webpage
def extract_links(url):
    response = requests.get(url, timeout=1)
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
                href = base_url + href
                links.append(href)
    return links

# Check if a link is already in the CSV file
def is_duplicate(url):
    with open('sites.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == url:
                return True
    return False

# Save links from the starting website to a CSV file
links = extract_links(start_url)
with open('sites.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for link in links:
        if not is_duplicate(link):
            writer.writerow([link])

# Crawl through all websites listed in the CSV file
while True:
    try:
        print("Another round!")
        with open('sites.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            url = list(reader)[count][0]
            links = extract_links(url)
            with open('sites.csv', 'a', newline='') as csvfile:
                count += 1
                writer = csv.writer(csvfile)
                for link in links:
                    if not is_duplicate(link):
                        writer.writerow([link])
        # Save the CSV file every 10 minutes
        #time.sleep(600)
    except Exception:
        print(f"Error, trying again")
        count += 1