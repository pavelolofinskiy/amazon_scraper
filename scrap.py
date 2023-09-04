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
    soup = BeautifulSoup(response.text, 'lxml')

    product_data_list = []

    # Find the parent element that contains the product listings
    parent = soup.find('div', class_='s-main-slot')

    variant_prices = []
    variant = parent.find_all('span', class_ = 'a-price a-text-price')
    for var in variant:
        price = var.find('span').text
        if price:
            variant_prices.append(price)
        else:
            variant_prices.append('N/A')
    
    reviews = []
    for review in parent.find_all('div', class_='a-row a-size-small'):
        aria_label = review.find('span', {'aria-label': True}).find_next_sibling()
        if aria_label:
            reviews.append(aria_label['aria-label'])
        else:
            reviews.append('N/A')

    # Extract product details
    products = parent.find_all('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'})
    prices = parent.find_all('span', class_='a-price-whole')
    stars = parent.find_all('span', class_='a-icon-alt')
    link1 = parent.find_all('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
    links = ['https://www.amazon.com' + element['href'] for element in link1]

    # Iterate over the products, prices, and stars and extract data
    for product, price, variant_price, star, link, review in zip(products, prices, variant_prices, stars, links, reviews):
        # Remove commas and dots from the price
        price_text = price.get_text().replace(',', '').replace('.', '')
        review_text = review.replace(',', '')
        product_data = {
            'Title': product.get_text(),
            'Price': price_text if price else 'N/A',
            'Variant Price': variant_price,
            'Stars': star.get_text() if star else 'N/A',
            'Link': link,
            'Reviews': review_text,
        }
        product_data_list.append(product_data)

    return product_data_list

# Specify the number of pages you want to scrape
num_pages = 1
base_url = 'https://www.amazon.com/s?k=ipad+pro&page={}'

all_product_data = []


# Now write the data to CSV file
with open('products.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Title','Price', 'Variant Price', 'Stars', 'Link', 'Reviews']  # Specify the fieldnames
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()  # Write the header

    for product_data in all_product_data:
        writer.writerow(product_data)