import requests
from bs4 import BeautifulSoup
import json

def scrape_quotes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    quotes = soup.find_all('div', class_='quote')

    quotes_data = []
    authors_data = []

    for quote in quotes:
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        author_url = url + quote.find('a')['href']

        quotes_data.append({
            'text': text,
            'author': author
        })

        if author not in [a['name'] for a in authors_data]:
            authors_data.append({
                'name': author,
                'url': author_url
            })

    return quotes_data, authors_data

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

base_url = 'http://quotes.toscrape.com'
quotes_data, authors_data = scrape_quotes(base_url)

next_page = True
page_number = 2

while next_page:
    page_url = base_url + '/page/' + str(page_number)
    new_quotes, new_authors = scrape_quotes(page_url)

    if new_quotes:
        quotes_data.extend(new_quotes)
        authors_data.extend([a for a in new_authors if a not in authors_data])
        page_number += 1
    else:
        next_page = False

save_to_json(quotes_data, 'quotes.json')
save_to_json(authors_data, 'authors.json')