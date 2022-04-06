# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 22:22:58 2022

@author: Carlos
"""
import requests
from bs4 import BeautifulSoup
import re
import time
import json


url = 'https://kriim.com/collections/all_collections'

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

# Ahora aquí hay que iterar para entrar en la info de cada producto
for product in productLinks[:5]:
    # como los enlaces no están completos
    # hay que concatenar el dominio con el string de la lista
    productUrl = 'https://kriim.com' + product
    productRequest = requests.get(productUrl, headers=headers)
    time.sleep(3)
    productSoup = BeautifulSoup(productRequest.content, 'lxml')
    # me bajo los atributos del producto según tag y clase
    name = productSoup.find('h1', attrs={'class': 'product-item-caption-title'})
    name = name.get_text()
    
    subtitle = productSoup.find('h3', attrs={'class': 'product-item-subtitle'})
    subtitle = subtitle.get_text()
    
    price = productSoup.find('span', attrs={'class': 'money', 'itemprop': 'price'})
    price = price.get_text()
    
    # Busco en product reviews
    productReviews = productSoup.find('div', attrs={'id': 'shopify-product-reviews'})
    # Aquí el problema es que las reviews
    # están en un script de js con formato JSON-LD
    reviewScripts = productReviews.find('script', type='application/ld+json').string
    # print(reviewScripts)
    data = json.loads(reviewScripts)
    # print(data['ratingValue'])
    ratingValue = data['ratingValue']
    numReviews = data['reviewCount']
