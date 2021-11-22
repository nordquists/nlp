from bs4 import BeautifulSoup
import requests
import pandas
import urllib.request
from random import sample

import time
import sys
import csv
import os

TEMP_SEARCH_RESULTS_CSV = 'sr.csv'
SAMPLED_PATENTS = 150

def clean_up():
    os.remove(TEMP_SEARCH_RESULTS_CSV)

def download_search_results(cpc):
    link = f"https://patents.google.com/xhr/query?url=q%3D({cpc})%26country%3DUS%26language%3DENGLISH%26oq%3D({cpc})%2Bcountry%3AUS%2Blanguage%3AENGLISH&exp=&download=true"

    # urllib.request.urlretrieve(link, TEMP_SEARCH_RESULTS_CSV, proxies={'http': 'https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc&protocols=http'})
    # requests.get(link)

    r = requests.get(link, allow_redirects=True)
    with open(TEMP_SEARCH_RESULTS_CSV, 'wb') as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)

def parse_patent_links(csv_file_name):
    data = pandas.read_csv(csv_file_name, skiprows=1)
    return sample(list(data['result link']), SAMPLED_PATENTS)

def parse_html(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, features="lxml")

    title = soup.find('h1', {"itemprop": "pageTitle"}).contents[0].split(' ')[0]
    info = soup.find_all('h1', {"itemprop": "pageTitle"})
    abstract = soup.find_all('section', {"itemprop": "abstract"})
    description = soup.find_all('section', {"itemprop": "description"})
    claims = soup.find_all('section', {"itemprop": "claims"})

    return title, info + abstract + description + claims

def save_html(output, soup):
    start = """
    <html>
        <body>
            <search-app>
                <article class="result" itemscope="" itemtype="http://schema.org/ScholarlyArticle">
    """
    end = """
                </article>
            </search-app>
        </body>
    </html>
    """

    for item in soup:
        start += str(item)

    full_html = start + end

    with open(output, "w") as file:
        file.write(full_html)

if __name__ == '__main__':
    query = sys.argv[1]
    download_search_results(query)

    csv_file_name = TEMP_SEARCH_RESULTS_CSV
    output_dir = sys.argv[2] if len(sys.argv) >= 3 else query
    file_list_name = sys.argv[3]  if len(sys.argv) >= 4 else query + '.txt'

    file_names = []

    links = parse_patent_links(csv_file_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for link in links:
        output_file, html = parse_html(link)
        save_html(f'./{output_dir}/{output_file}.html', html)
        file_names.append(f'{output_dir}/{output_file}.html')
    
    with open(f'./{output_dir}/{file_list_name}', "w") as file:
        for line in file_names:
            file.write(line + '\n')

    clean_up()
