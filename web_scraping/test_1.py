from urllib.request import urlopen as uReq
import csv
from bs4 import BeautifulSoup as soup

my_url = 'https://www.newegg.com/global/ru-en/Video-Cards-Video-Devices/Category/ID-38'

#opening up connection, grabbing the page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# html parsing
page_soup = soup(page_html, "html.parser")
#grabs each product
containers = page_soup.findAll("div",{"class":"item-info"})

f = open("videocards.csv", "w")

with f:

	fnames = ['brand', 'product_name']
	writer = csv.DictWriter(f, fieldnames=fnames)
	writer.writeheader()

# headers = "brand, product_name\n"

# f.write("headers")

	for container in containers:
		brand = container.div.a.img["title"]

		title_container = container.findAll("a",{"class":"item-title"})
		product_name = title_container[0].text

		print("brand: " + brand)
		print("product name: " + product_name)

		f.write(brand + ", " + product_name.replace(",", "|") + "\n")

	f.close()

