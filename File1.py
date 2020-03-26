import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

URL = "https://www.flipkart.com/laptops/pr?sid=6bo,b5g&marketplace=FLIPKART"
response = requests.get(URL)
content = response.content
soup = BeautifulSoup(content, "html.parser")

products = []  # List to store name of the product
prices = []  # List to store price of the product

for a in soup.findAll('a', href=True, attrs={'class': '_31qSD5'}):
    name = a.find('div', attrs={'class': '_3wU53n'})
    cost = a.find('div', attrs={'class': '_1vC4OE _2rQ-NK'})
    cost_str = cost.text
    pattern = re.compile(r"(\d+,?\d*\.?\d*)")
    match = pattern.search(cost_str)
    found_cost = match.group(1).replace(",", "")
    price = float(found_cost)
    products.append(name.text)
    prices.append(price)

df = pd.DataFrame({'Product Name': products, 'Price': prices})
df.to_csv('products.csv', index=False, encoding='utf-8')

max_price = 25000
index = df[df['Price'] < max_price].index.tolist()
df2 = df.iloc[index]
df2.to_csv('SelectedProducts.csv', index=False, encoding='utf-8')
print("Laptops below Rs.", max_price, " are:")
print(df2)


