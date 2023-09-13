from bs4 import BeautifulSoup

with open('amazon_page.html', 'r', encoding='utf-8') as html_file:
    html_content = html_file.read()

soup = BeautifulSoup(html_content, 'lxml')

parent = soup.find('div', class_='css-1dbjc4n')
print(parent)

def scraper():
    result = {}  # Create an empty dictionary to store the results
    

    if parent:
        result['stars'] = None

        try:
            stars = parent.find('span', class_='a-icon-alt')
            result['stars'] = stars.text  # Store the reviews in the dictionary
        except (AttributeError, ValueError) as s:
            print(s)

all_data = scraper()
print(all_data)
    