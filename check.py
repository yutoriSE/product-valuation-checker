from engine import amazonserch, sakurachecker
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from common import desktop, driver_generator, logger_generator

# webdriver生成
driver = driver_generator.set_driver(test_flag=True)

driver.get('https://www.amazon.co.jp/%E3%82%BD%E3%83%8B%E3%83%BC-SONY-%E3%83%98%E3%83%83%E3%83%89%E3%83%9B%E3%83%B3-MDR-ZX310-%E6%8A%98%E3%82%8A%E3%81%9F%E3%81%9F%E3%81%BF%E5%BC%8F/dp/B00HZD3UFM/ref=sr_1_437?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&dchild=1&keywords=sony&qid=1620919016&sr=8-437')

price = driver.find_element_by_id('price').text
if '\n' in price:
    price = price[:price.find('\n')]
price = price[price.find('￥')+1:].replace(',', '')


print(price)
driver.close()
