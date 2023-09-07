from bs4 import BeautifulSoup

with open('amazon_page.html', 'r', encoding='utf-8') as html_file:
    html_content = html_file.read()

soup = BeautifulSoup(html_content, 'lxml')

parent = soup.find('div', class_='a-container')
price = soup.find('div', class_='apex_desktop')
print(price)

def scraper():
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
            print(price1)
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

all_data = scraper()
print(all_data)
    