from bs4 import BeautifulSoup

with open('twitter_page.html', 'r', encoding='utf-8') as html_file:
    html_content = html_file.read()

soup = BeautifulSoup(html_content, 'lxml')

parent = soup.find('div', class_='css-1dbjc4n')
print(parent)

def scraper():
    result = {}  # Create an empty dictionary to store the results
    



    return result

all_data = scraper()
print(all_data)
    