"""
This code is bot to add item to the cart and scrap information
from Nike (www.nike.com) and Uniqlo (www.uniqlo.com)
"""

from selenium import webdriver
import config_example2 as config
import nike_process
import uniqlo_process


options = webdriver.ChromeOptions()
options.add_argument("incognito")
options.add_argument("start-maximized")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options, executable_path='chromedriver3.exe')
driver.execute_script(
    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_cdp_cmd(
    'Network.setUserAgentOverride', {
        "userAgent":
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'\
        '(KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'})


def main():
    global driver

    url_target = config.start_url
    if (url_target.__contains__("nike.com")):
        nike_process.nike_process(url_target, driver, config)
    elif (url_target.__contains__("uniqlo.com")):
        uniqlo_process.uniqlo_process(url_target, driver, config)


# Lunch the main
main()
