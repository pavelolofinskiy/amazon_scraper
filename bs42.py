from bs4 import BeautifulSoup


with open('amazon_page.html', 'r', encoding='utf-8') as html_file:
    html_content = html_file.read()

soup = BeautifulSoup(html_content, 'lxml')

parent = soup.find('div', class_ = 'sg-col-20-of-24 s-matching-dir sg-col-16-of-20 sg-col sg-col-8-of-12 sg-col-12-of-16')

variant = parent.find_all('span', class_ = 'a-price a-text-price')
for var in variant:
    price = var.find('span')
    print(price.text)

