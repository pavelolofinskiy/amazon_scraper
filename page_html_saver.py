import requests
from bs4 import BeautifulSoup


def scrape_page_and_save_html(url, output_file):
    payload = {
        'api_key': '9d48909da2144bc72f125ac753ef5da4',
        'url': url
    }
    response = requests.get('http://api.scraperapi.com', params=payload)
    soup = BeautifulSoup(response.text, 'lxml')


    with open(output_file, 'w', encoding='utf-8') as html_file:
        html_file.write(str(soup))

url_to_scrape = 'https://www.amazon.com/Apple-11-inch-iPad-Pro-Wi-Fi-128GB/dp/B0BJLF3RR3/ref=sr_1_6?crid=1XG0IGZ5KOXYM&keywords=ipad&qid=1693903429&sprefix=ipad%2Caps%2C247&sr=8-6&th=1'

output_html_file = 'amazon_page.html'

scrape_page_and_save_html(url_to_scrape, output_html_file)