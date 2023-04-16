import requests
import json
import os
from bs4 import BeautifulSoup

product_id = input("Enter the product ID: ")
url = f"https://www.ceneo.pl/{product_id}#tab=reviews"
response = requests.get(url)
first = True

