import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool

def links_scraper():
    base_url = 'https://www.amazon.com/s?k=ipad+pro&page='

    all_links = []

    page_number = 1
    while True:
        url = f'{base_url}{page_number}'
        payload = {
            'api_key': '9d48909da2144bc72f125ac753ef5da4',
            'url': url
        }
        response = requests.get('http://api.scraperapi.com', params=payload)
        soup = BeautifulSoup(response.text, 'lxml')
        parent = soup.find('div', class_='sg-col-20-of-24 s-matching-dir sg-col-16-of-20 sg-col sg-col-8-of-12 sg-col-12-of-16')

        links = parent.find_all('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')

        if not links:
            break  # No more links found, exit the loop

        for element in links:
            link_element = element.get('href')
            link = 'https://www.amazon.com' + link_element
            all_links.append(link)

        page_number += 1  # Move to the next page

    return all_links

def amazon_scraper(url):
    num = 0

    payload = {
        'api_key': '9d48909da2144bc72f125ac753ef5da4',
        'url': url
    }
    response = requests.get('http://api.scraperapi.com', params=payload)
    soup = BeautifulSoup(response.text, 'lxml')
    parent = soup.find('div', class_ = 'a-container')
    
    result = {}  # Create an empty dictionary to store the results
    
    if parent:
        result['title'] = None

        try:
            title = parent.find('span', class_='a-size-large product-title-word-break') 
            result['title'] = title.text.strip()  # Store the title in the dictionary
        except (AttributeError, ValueError) as s:
            print(s)
    
    if parent:
        result['reviews'] = None

        try:
            reviews = parent.find('span', id='acrCustomerReviewText')
            result['reviews'] = reviews.text  # Store the reviews in the dictionary
        except (AttributeError, ValueError) as s:
            print(s)


    if parent:
        result['price'] = None  # Initialize the 'price' key to an empty string
        
        try:
            price1 = parent.find('div', id='corePrice_desktop')
            if price1:
                price = price1.find('span', class_ = 'a-offscreen')
                result['price'] = price.text   # Store the price in the dictionary, or an empty string if None
        except (AttributeError, ValueError) as s:
            print(s)


    if parent:
        result['variant_price'] = None

        try:
            price2 = parent.find('span', class_='a-price a-text-price a-size-base')
            variant_price = price2.find('span', class_='a-offscreen')
            result['variant_price'] = variant_price.text
        except (AttributeError, ValueError)as s:
            print(s)
    
    if parent:
        result['stars'] = None

        try:
            stars = parent.find('span', class_='a-icon-alt')
            result['stars'] = stars.text  # Store the reviews in the dictionary
        except (AttributeError, ValueError) as s:
            print(s)
        
    if parent:
        result['img_link'] = None

        try:
            img_link = parent.find('img', id='landingImage').get('src')
            result['img_link'] = img_link  # Store the reviews in the dictionary
        except (AttributeError, ValueError) as s:
            print(s)

    if parent:
        result['availability'] = None

        try:
            availability = parent.find('span', class_='a-size-base a-color-price a-text-bold')
        
            if availability is None:
                result['availability'] = 'Currently unavailable'
            else:
                availability_text = availability.text.strip()
                result['availability'] = availability_text
        except (AttributeError, ValueError) as s:
            print(s)


    return result

def scrape_product(link):
    data = amazon_scraper(link)
    return data

if __name__ == "__main__":
    all_links = links_scraper()  # Scrape pages until there are no more pages

    # Define the number of processes (adjust as needed)
    num_processes = 4

    with Pool(num_processes) as pool:
        scraped_data = pool.map(scrape_product, all_links)

    # Define the CSV file name
    csv_file = 'amazon_products.csv'

    # Define the CSV header
    csv_header = ['title', 'reviews', 'price', 'variant_price', 'stars', 'img_link', 'availability']

    # Write the data to the CSV file
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=csv_header)
        writer.writeheader()  # Write the header row

        for data in scraped_data:
            writer.writerow(data)