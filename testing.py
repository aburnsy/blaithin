from requests_html import HTMLSession
from bs4 import BeautifulSoup
from urllib.parse import urljoin

session = HTMLSession()
URL = 'https://shop.tullynurseries.ie/Product/Browse.aspx?Code=Topiary'
page = session.get(URL)

content = BeautifulSoup(page.content, "html.parser")
product_table = content.find("table", class_="productsGridView")
products = product_table.find_all('tr')
for product in products[1:]:
    product_name = product.find('p', class_= 'productName').text
    product_code = product.find('p', class_= 'productCode').find('span').text
    image = product.find('div', class_= 'imageWrap').find('img')
    img_url = urljoin(URL, image['src']).rsplit('&Thumbnail=true', 1)[0]
    description = product.find('p', class_= 'description').find('span').text
    price_vat_exc = product.find('div', class_ = 'priceVatExcCurrencySymbol').find_all('span')[1].text
    price = round(float(price_vat_exc) * 1.135, 2)
    size = product.find('div', class_ = 'columnField').find('span').text  
    stock = int(product.find('div', class_ = 'inStock').text)
    
    print(product_name)
    print(product_code)
    print(img_url)
    print(description)
    print(price_vat_exc)
    print(price)
    print(size)
    print(stock)
    break
exit