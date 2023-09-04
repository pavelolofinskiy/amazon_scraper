import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape data from a single page
def scrape_page(url):
    payload = {
        'api_key': '9d48909da2144bc72f125ac753ef5da4',
        'url': url
    }
    response = requests.get('http://api.scraperapi.com', params=payload)
    soup = BeautifulSoup(response.text, 'html.parser')  # Changed 'lxml' to 'html.parser'

    product_data_list = []

    products = soup.find_all('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'})
    prices = soup.find_all('span', class_='a-price-whole')
    stars = soup.find_all('span', class_='a-icon-alt')
    link1 = soup.find_all('a', class_ = 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
    links = [element['href'] for element in link1]

    # Iterate over the products, prices, and stars and extract data
    for product, price, star, link in zip(products, prices, stars, links):
        product_data = {
            'Title': product.get_text(),
            'Price': price.get_text(),
            'Stars': star.get_text(),
            'Link': link,
        }
        product_data_list.append(product_data)

    return product_data_list

# Specify the number of pages you want to scrape
num_pages = 1
base_url = 'https://www.amazon.com/s?k=ipad+pro&page={}'

all_product_data = []

# Loop through the pages and scrape data
for page in range(1, num_pages + 1):
    page_url = base_url.format(page)
    product_data_list = scrape_page(page_url)
    all_product_data.extend(product_data_list)

# Now write the data to CSV file
with open('products.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Title', 'Price', 'Stars', 'Link']  # Specify the fieldnames
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()  # Write the header

    for product_data in all_product_data:
        writer.writerow(product_data)