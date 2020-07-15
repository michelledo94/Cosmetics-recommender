import platform
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

supported_platforms = {
                'Linux': 'bin/chromedriver_linux64/chromedriver',
                'Darwin': 'bin/chromedriver_mac64/chromedriver',
                'Windows': 'bin/chromedriver_win32/chromedriver.exe',
              }

driver_path = supported_platforms.get(platform.system(), "Unsupported platform.")

if driver_path == 'Unsupported platform.':
    print('Error:', driver_path)
    sys.exit(1)

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
chromeOptions.add_argument("--no-sandbox")
chromeOptions.add_argument("--disable-setuid-sandbox")
chromeOptions.add_argument("--remote-debugging-port=9222")
chromeOptions.add_argument("--disable-dev-shm-using")
chromeOptions.add_argument("--disable-extensions")
chromeOptions.add_argument("--disable-gpu")
chromeOptions.add_argument("start-maximized")
chromeOptions.add_argument("disable-infobars")
chromeOptions.add_argument("--headless")
driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chromeOptions)
driver.get('https://www.google.com/')
time.sleep(5)
driver.quit()
