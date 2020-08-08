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
        if 'ulta' in site:
            self.categories = WebScraper.ulta_categories
        self.driver = webdriver.Chrome(executable_path=binary_path)

    def scrape_category_links(self, navigation_xml):
        links = []
        response = requests.get(navigation_xml)
        tree = ET.fromstring(response.content)
        for url in tree:
            for i in self.categories.values():
                if i in url[0].text:
                    links.append(url[0].text)

        return links

    def scrape_product_links(self, category_page):
        links = []
        self.driver.get(category_page)
        content = self.driver.page_source
        products = self.driver.find_elements_by_class_name('productQvContainer')
        for product in products:
            try:
                ref = product.find_element_by_tag_name('a').get_attribute('href')
                links.append(ref)
            except selenium.common.exceptions.NoSuchElementException:
                continue
        return links


if __name__ == '__main__':
    ws = WebScraper(platform.system(), 'https://www.ulta.com/')
    try:
        category_pages = ws.scrape_category_links('https://www.ulta.com/navigation0.xml')
        for page in category_pages:
            product_links = ws.scrape_product_links(page)
            print(product_links)
    finally:
        ws.driver.quit()
