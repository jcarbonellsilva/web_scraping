import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.freshlycosmetics.com/es/productos/'

productLinks = []

r = requests.get(url)

soup = BeautifulSoup(r.content, 'lxml')

productList = soup.find_all('h2', class_ ='h3 product-title')

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'
}

for item in productList:
    for link in item.find_all('a', href=True):
        productLinks.append(link['href'])

productFinal = []
for link in productLinks:
    r = requests.get(link,headers = headers)
    soup = BeautifulSoup(r.content, 'lxml')

    try:
        name = soup.find('h1', class_='p-0 product-title').text.strip()
    except:
        name = soup.find('h1', class_ = 'p-0 product-title fc-margin-b-15').text.strip()

    try:
        use = soup.find('h2', class_ = 'subtitle').text.strip()
    except:
        use = 'no_use'
    
    current_price = soup.find('span', class_ = 'gtm_price auto-update-price fc-font-s-26').text.strip()
    
    try:
        current_discount = soup.find('span', class_ = 'descompte-actual dto-percentage auto-update-percentage').text.strip()
    except:
        current_discount = 'no_discount'

    try:
        review = soup.find('span', class_ = 'fc-font-w-700').text.strip()
    except:
        review = 'no_review'

    try:
        opinions = soup.find('span', class_ = 'fc-color-black fc-margin-l-5 trustpilot-total-opiniones').text.strip()
    except:
        opinions = 'no_opinions'

    freshly = {
        'site': 'freshly',
        'name': name,
        'use': use,
        'current_price': current_price,
        'current_discount': current_discount,
        'review': review,
        'opinions': opinions
    }

    productFinal.append(freshly)

df = pd.DataFrame(productFinal)

df.to_csv('dataFreshly.csv')
print('saved to file')