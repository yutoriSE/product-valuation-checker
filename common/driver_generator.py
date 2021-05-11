from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def set_driver(test_flag):
    option = Options()
    if not test_flag:
        option.add_argument('--headless')
    option.add_argument('--ignore-certificate-errors')
    option.add_argument('--ignore-ssl-errors')
    option.add_argument('--incognito')

    return webdriver.Chrome(ChromeDriverManager().install(), options=option)
