import requests
from bs4 import BeautifulSoup


def scrape_page_and_save_html(url, output_file):
    payload = {
        'api_key': '9d48909da2144bc72f125ac753ef5da4',
        'url': url
    }
    response = requests.get('https://twitter.com/CNN')
    soup = BeautifulSoup(response.text, 'lxml')


    with open(output_file, 'w', encoding='utf-8') as html_file:
        html_file.write(str(soup))

url_to_scrape = 'https://twitter.com/CNN'

output_html_file = 'twitter_page.html'

scrape_page_and_save_html(url_to_scrape, output_html_file)