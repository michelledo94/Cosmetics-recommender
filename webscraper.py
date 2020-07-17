import platform
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

class WebScraper:
    def initialize_driver():
        supported_platforms = {
                                'Linux': 'bin/chromedriver_linux64/chromedriver',
                                'Darwin': 'bin/chromedriver_mac64/chromedriver',
                                'Windows': 'bin/chromedriver_win32/chromedriver.exe',
                              }
        driver_path = supported_platforms.get(platform.system(), "Unsupported platform.")
        if driver_path == 'Unsupported platform.':
            print('Error:', driver_path)
            sys.exit(1)
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
        driver = webdriver.Chrome(executable_path=driver_path, options=options)
        return driver

if __name__ == '__main__':
    driver = WebScraper.initialize_driver()
    driver.get('https://www.ulta.com/navigation0.xml')
    content = driver.page_source
    print(content)
    driver.quit()
