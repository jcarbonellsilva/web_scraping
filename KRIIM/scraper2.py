# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json

# URL is anonimized in order to preserve the owner's data policy
url = 'site_url'

productLinks = []

# Lanzar petición a la web

r = requests.get(url, allow_redirects=True)

# Creo el objeto de BeautifulSoup

soup = BeautifulSoup(r.content, 'lxml')

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
    }

# Busco todos los links a productos a través de inspeccionar el elemento de la lista de productos
rawProductLinks = soup.find_all('a', attrs={'class': "product-thumb-href"})
productLinks = [link['href'] for link in rawProductLinks]
# aquí me quedo sólo con los valores únicos, ya que los enlaces se leen dos veces
productLinks = list(set(productLinks))
productFinal = []
# Ahora aquí hay que iterar para entrar en la info de cada producto
for product in productLinks:
    # como los enlaces no están completos
    # hay que concatenar el dominio con el string de la lista
    productUrl = 'site_main' + product
    productRequest = requests.get(productUrl, headers=headers)
    time.sleep(3)
    productSoup = BeautifulSoup(productRequest.content, 'lxml')
    # me bajo los atributos del producto según tag y clase
    try:
        name = productSoup.find('h1', attrs={'class': 'product-item-caption-title'})
        name = name.get_text()
    except:
        name = "unknown"
    
    try:
        subtitle = productSoup.find('h3', attrs={'class': 'product-item-subtitle'})
        subtitle = subtitle.get_text()
    except:
       subtitle = "unknown"
       
    try:
        price = productSoup.find('span', attrs={'class': 'money', 'itemprop': 'price'})
        price = price.get_text()
        
    except:
        price = "not available"
    
    try:
        # Busco en product reviews
        productReviews = productSoup.find('div', attrs={'id': 'shopify-product-reviews'})
        # Aquí el problema es que las reviews
        # están en un script de js con formato JSON-LD
        reviewScripts = productReviews.find('script', type='application/ld+json').string
        data = json.loads(reviewScripts)
        ratingValue = data['ratingValue']
        numReviews = data['reviewCount']
        current_discount = data['itemReviewed']['offers']['lowPrice']
    except:
        ratingValue = "unknown"
        numReviews = "unknown"
        current_discount = "no discount"

    products = {
        'site': "site 2",
        'name': name,
        'use': subtitle,
        'current_price': price,
        'current_discount': current_discount,
        'review': ratingValue,
        'opinions': numReviews,
        'images': "non available"
    }
    productFinal.append(products)

df = pd.DataFrame(productFinal)
df.to_csv('site2Table.csv')
print('saved to file')
