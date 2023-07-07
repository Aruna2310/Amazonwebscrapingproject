import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2CC283&ref=sr_pg_1'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

product_name_list = []
product_url_list = []
price_list = []
rating_list = []
reviews_count_list = []

for page in range(1, 21):
    url = f'https://www.amazon.in/s?k=bags&page={page}&qid=1653308124&ref=sr_pg_{page}'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    for i in soup.findAll('div', attrs={'class': 's-result-item'}):
        try:
            product_name = i.find('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()
        except:
            product_name = None

        try:
            product_url = "https://www.amazon.in" + i.find('a', href=True)['href']
        except:
            product_url = None

        try:
            price_parent_node = i.find('span', attrs={'class': 'a-price-whole'})
            price = price_parent_node.text.strip() + '.' + price_parent_node.find_next_sibling().text.strip()
        except:
            price = None

        try:
            rating = i.find('span', attrs={'class': 'a-icon-alt'}).text.strip()
        except:
            rating = None

        try:
            reviews_count = i.find('span', attrs={'class': 'a-size-base'}).text.strip()
        except:
            reviews_count = None

        product_name_list.append(product_name)
        product_url_list.append(product_url)
        price_list.append(price)
        rating_list.append(rating)
        reviews_count_list.append(reviews_count)

data_dict = {'Product Name': product_name_list,
             'Product URL': product_url_list,
             'Product Price': price_list,
             'Product Rating': rating_list,
             'Number of Reviews': reviews_count_list}

df = pd.DataFrame(data_dict)

df.to_csv('amazon_products.csv', index=False)

