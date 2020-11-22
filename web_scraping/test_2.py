from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
import numpy as np
string1 = []
string2 = []
string3 = []

for i in range(1,7):
    my_url = 'https://www.newegg.com/global/ru-en/p/pl?Submit=StoreIM&page=' + str(i) + '&Depa=1&Category=38'
    print("page = " + str(i))
    #opening up connection, grabbing the page
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    
    # html parsing
    page_soup = soup(page_html, "html.parser")
    #grabs each product
    containers = page_soup.findAll("div",{"class":"item-info"})
        
    for container in containers:
        brand = container.div.a.img["title"]
        title_container = container.findAll("a",{"class":"item-title"})
        product_name = title_container[0].text
        product_name = product_name.replace(",", "|")
        price_container = container.findAll("li",{"class":"price-current"})
        price_text = price_container[0].text
        price = re.sub("[^0-9]","", price_text)
        string1 = (brand, product_name, price)
        string2 = list(string1)
        string3.append(string2)

np.savetxt("allvideocards.csv", string3, delimiter=",", fmt='%s')            
            




