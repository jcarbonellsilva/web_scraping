# -*- coding: utf-8 -*-

# =============================================================================
# Solo para uso personal. No se permiten usos comerciales de este script ni de
# los datos que se obtienen.
# =============================================================================

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json


url = 'https://kriim.com/collections/all_collections'

productLinks = []

# Lanzar petición a la web

r = requests.get(url, allow_redirects=True)

# Creo el objeto de BeautifulSoup para leer el contenido de la web

soup = BeautifulSoup(r.content, 'lxml')

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
    }

# Busco todos los links a productos a través de inspeccionar el elemento 
# de la lista de productos
rawProductLinks = soup.find_all('a', attrs={'class': "product-thumb-href"})
productLinks = [link['href'] for link in rawProductLinks]
# aquí me quedo sólo con los valores únicos, ya que los enlaces se leen dos veces
productLinks = list(set(productLinks))
productFinal = []
# Ahora aquí hay que iterar para entrar en la url con la info de cada producto
for product in productLinks:
    # como los enlaces no están completos
    # hay que concatenar el dominio con el string de la lista
    productUrl = 'https://kriim.com' + product
    productRequest = requests.get(productUrl, headers=headers)
    # Esta pausa es bastante mayor al tiempo de respuesta de la web
    # Por tanto, espacia las peticiones
    time.sleep(3)
    # Para el enlace de cada producto, leo el contenido de la página
    productSoup = BeautifulSoup(productRequest.content, 'lxml')
    # Me bajo los atributos del producto según tag y clase
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
        # Al parsearlo con la libreria json, consigo transformar el script
        # en un formato de diccionario
        data = json.loads(reviewScripts)
        # Para extraer los datos, solo tengo que buscar el valor de la clave
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
        # Por tema de la propiedad de los datos
        # no bajo las imágenes de esta web
        'images': "non available"
    }
    productFinal.append(products)

df = pd.DataFrame(productFinal)
df.to_csv('site2Table.csv')
print('saved to file')
