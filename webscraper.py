import xml.etree.ElementTree as ET 
import platform
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from chromedriver_py import binary_path
import time
import sys

class WebScraper:
    ulta_categories = {
                        'Moisturizer': 'skin-care-moisturizers', 
                        'Cleanser': 'skin-care-cleansers',
                        'Treatment': 'skin-care-treatment-serums-acne-blemish-treatments',
                        'Face Mask': 'skin-care-treatment-serums-face-masks',
                        'Eye cream': 'skin-care-eye-treatments-eye-cream',
                        'Sun protect': 'skin-care-suncare-sunscreen'
                      }

    def __init__(self, platform, site):
        self.site = site
        self.catalog = {}
        if 'ulta' in site:
            self.store = 'ulta'
            self.categories = WebScraper.ulta_categories
        self.driver = webdriver.Chrome(executable_path=binary_path)

    def scrape_category_links(self, navigation_xml):
        links = []
        response = requests.get(navigation_xml)
        tree = ET.fromstring(response.content)
        for url in tree:
            for category in self.categories:
                if self.categories[category] in url[0].text:
                    links.append((category, url[0].text))

        return links

    def scrape_product_links(self, category_page):
        links = []
        self.driver.get(category_page)
        products = self.driver.find_elements_by_class_name('productQvContainer')
        for product in products:
            try:
                ref = product.find_element_by_tag_name('a').get_attribute('href')
                links.append(ref)
            except selenium.common.exceptions.NoSuchElementException as e:
                print('Error in scrape_product_links:', category_page, e)
                continue
        return links

    def scrape_product_details(self, product_page):
        self.driver.get(product_page)
        try:
            brand = self.driver.find_element_by_xpath("//div[@class='ProductMainSection__brandName']").find_element_by_tag_name('p').text
            name = self.driver.find_element_by_xpath("//div[@class='ProductMainSection__productName']").find_element_by_tag_name('span').text
            price = self.driver.find_element_by_xpath("//div[@class='ProductPricingPanel']").find_element_by_tag_name('span').text.split('$')[1]
            rating = self.driver.find_element_by_xpath("//div[@class='RatingPanel']").find_element_by_xpath(".//label[@class='sr-only']").text
            ingredient_sect = self.driver.find_element_by_xpath("//div[@class='ProductDetail__ingredients']")
            ingredients = '"' + ingredient_sect.find_element_by_xpath(".//div[@class='ProductDetail__productContent']").get_attribute('textContent') + '"'
        except selenium.common.exceptions.NoSuchElementException as e:
            print('Error in scrape_product_details', product_page, e)
            return None

        return [brand, name, price, rating, ingredients]

if __name__ == '__main__':
    ws = WebScraper(platform.system(), 'https://www.ulta.com/')
    try:
        category_pages = ws.scrape_category_links('https://www.ulta.com/navigation0.xml')
        for category, page in category_pages:
            product_links = ws.scrape_product_links(page)
            for product in product_links:
                details = ws.scrape_product_details(product)
                if details:
                    with open(ws.store + '.csv', 'a') as f:
                        f.write(','.join([category] + details) +'\n')
    finally:
        ws.driver.quit()
