import os
import eel
import pandas as pd
from engine import amazonserch, sakurachecker
from common import desktop, driver_generator, logger_generator

# アプリ設定
APP_NAME = 'web'
END_POINT = 'index.html'
SIZE = (1200, 800)

# ログ設定
logger = logger_generator.set_logger()

# webdriver生成
driver = driver_generator.set_driver(test_flag=True)

# amazonインスタンスの生成
amazon = amazonserch.Amazon(driver, logger)

# sakuraインスタンスの生成
sakura = sakurachecker.Sakura(driver, logger)


# amazonのキーワード検索実行
@eel.expose
def fetch_products_info(keyword):
    logger.debug('fetch_products_info was executed')

    # amazonでキーワード検索
    amazon.fetch_products_data(keyword)

    # サクラチェッカーで商品毎の評価取得（前回と同じキーワードの場合はスキップ）
    if not keyword == amazon.keyword:
        sakura.fetch_producs_valuation(amazon.products, amazon.keyword)
    else:
        logger.debug('fetch_products_info was skipped')

    return sakura.valuations


# 入力されたパスで出力
@eel.expose
def export_data(path):
    logger.debug('export_data was executed')
    data = amazon.products
    df = pd.DataFrame(data, columns=[])
    try:
        df.to_excel(path)
    except:
        logger.debug('pathエラー')


# サクラチェッカーのデータをロード
@eel.expose
def load_valuation():
    if sakura.executed_flag:
        return sakura.valuations
    else:
        logger.debug('instance of sakura does not have valuations')


# サクラチェッカーのキーワードをロード
@eel.expose
def load_keyword():
    return sakura.keyword


# アプリ起動
desktop.start(appName=APP_NAME, endpoint=END_POINT, size=SIZE)
logger.debug('desktop was created')
