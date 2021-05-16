from engine import amazonserch, sakurachecker
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from common import desktop, driver_generator, logger_generator

# webdriver生成
driver = driver_generator.set_driver(test_flag=True)

driver.get('https://sakura-checker.jp/search/B08FZJY9K1/')

text = driver.find_element_by_class_name('sakura-num').text


print(text)
driver.close()
