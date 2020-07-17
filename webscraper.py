import xml.etree.ElementTree as ET 
import platform
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from chromedriver_py import binary_path
import time

class WebScraper:
    def __init__(self, platform):
        self.driver = webdriver.Chrome(executable_path=binary_path)

    def scrape_category_links(navigation_xml):
        links = []
        response = requests.get(navigation_xml)
        tree = ET.fromstring(response.content)
        print(tree.tag)
        for url in tree:
            links.append(url[0].text)
        return links

    def scrape_product_links(self, category_page):
        links = []
        self.driver.get(category_page)
        content = self.driver.page_source
        print(content)
        return links


if __name__ == '__main__':
    ws = WebScraper(platform.system())
    category_pages = WebScraper.scrape_category_links('https://www.ulta.com/navigation0.xml')
    for page in category_pages:
        product_links = ws.scrape_product_links(page)