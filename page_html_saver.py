import requests
from bs4 import BeautifulSoup


def scrape_page_and_save_html(url, output_file):
    payload = {
        'api_key': '9d48909da2144bc72f125ac753ef5da4',
        'url': url
    }
    response = requests.get('https://www.amazon.com/Apple-iPad-Pro-12-9in-Gen/dp/B0BFC578CR/ref=sr_1_72?keywords=ipad+pro&qid=1694597740&sr=8-72')
    soup = BeautifulSoup(response.text, 'lxml')


    with open(output_file, 'w', encoding='utf-8') as html_file:
        html_file.write(str(soup))

url_to_scrape = 'https://twitter.com/CNN'

output_html_file = 'amazon_page.html'

scrape_page_and_save_html(url_to_scrape, output_html_file)