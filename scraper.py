import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool

def links_scraper(pages_to_scrape=10):
    base_url = 'https://www.amazon.com/s?k=ipad+pro&page='

    all_links = []
 

    for page_number in range(1, pages_to_scrape + 1):
        url = f'{base_url}{page_number}'
        payload = {
            'api_key': 'bb199daad9be81ce5c5e39feb9bc9489',
            'url': url
        }
        response = requests.get('http://api.scraperapi.com', params=payload)
        soup = BeautifulSoup(response.text, 'lxml')
        parent = soup.find('div', class_='sg-col-20-of-24 s-matching-dir sg-col-16-of-20 sg-col sg-col-8-of-12 sg-col-12-of-16')

        links = parent.find_all('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')

        for element in links:
            link_element = element.get('href')
            link = 'https://www.amazon.com' + link_element
            all_links.append(link)


    return all_links[:pages_to_scrape * 24]

def amazon_scraper(url):


    payload = {
        'api_key': 'bb199daad9be81ce5c5e39feb9bc9489',
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
        result['stars'] = None

        try:
            stars = parent.find('span', class_='a-icon-alt')
            if stars.text == 'Previous page':
                result['stars'] = None
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
    csv_header = ['title', 'reviews', 'price', 'stars', 'img_link', 'availability']

    # Write the data to the CSV file
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=csv_header)
        writer.writeheader()  # Write the header row

        for data in scraped_data:
            writer.writerow(data)