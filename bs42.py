from bs4 import BeautifulSoup


with open('amazon_page.html', 'r', encoding='utf-8') as html_file:
    html_content = html_file.read()

soup = BeautifulSoup(html_content, 'lxml')


link = soup.find_all('a', class_ = 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
links = [element['href'] for element in link]
for title in links:
    s = 'www.amazon.com' + title
    print(s)
        