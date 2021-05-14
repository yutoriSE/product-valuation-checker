import threading
import traceback
from engine import amazonserch, sakurachecker
from common import desktop, driver_generator, logger_generator

# ログ設定
logger = logger_generator.set_logger()

# webdriver生成
driver = driver_generator.set_driver(test_flag=True)

# amazonインスタンスの生成
amazon = amazonserch.Amazon(driver, logger)

# sakuraインスタンスの生成
sakura = sakurachecker.Sakura(driver)

try:
    amazon.fetch_products_data('MateBook 13')
except:
    logger.debug(f'異常終了：{traceback.format_exc()}')
