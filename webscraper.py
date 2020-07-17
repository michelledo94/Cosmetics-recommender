import xml.etree.ElementTree as ET 
import platform
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

class WebScraper:
    def __init__(self, platform):
        supported_platforms = {
                                'Linux': 'bin/chromedriver_linux64/chromedriver',
                                'Darwin': 'bin/chromedriver_mac64/chromedriver',
                                'Windows': 'bin/chromedriver_win32/chromedriver.exe',
                              }
        driver_path = supported_platforms.get(platform, "Unsupported platform.")
        if driver_path == 'Unsupported platform.':
            print('Error:', driver_path)
            raise Exception('Unsupported platform')
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--disable-dev-shm-using")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path=driver_path, options=options)

    def scrape_category_links(navigation_xml):
        links = []
        response = requests.get(navigation_xml)
        tree = ET.fromstring(response.content)
        print(tree.tag)
        for url in tree:
            links.append(url[0].text)
        return links

if __name__ == '__main__':
    # ws = WebScraper(platform.system())
    links = WebScraper.scrape_category_links('https://www.ulta.com/navigation0.xml')
    print(links)
