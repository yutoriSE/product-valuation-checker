from logging import Logger, debug
import pandas as pd
import threading
import traceback
import time
import os
import sys
from webdriver_manager import driver, logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs4
from common import driver_generator


URL = 'https://www.amazon.co.jp/'
THREAD_NUM = 15


# selenium利用
class Amazon():

    def __init__(self, driver: webdriver.Chrome, logger: Logger):
        self.__keyword = ''
        self.__products = []  # 二次元 [ [商品名, 価格, 星, 画像URL, URL], ・・・ ]
        self.driver = driver
        self.__executed_flag = False
        self.logger = logger

    @property
    def products(self):
        return self.__products

    @property
    def keyword(self):
        return self.__keyword

    @keyword.setter
    def keyword(self, keyword):
        self.__keyword = keyword

    @property
    def executed_flag(self):
        return self.__executed_flag

    # 商品ページの詳細を取得
    def fetch_details_info(self, urls):

        try:
            thread_driver = driver_generator.set_driver(test_flag=False)
            temp_products = []

            for url in urls:
                try:
                    thread_driver.get(url)

                    # 読み込み待機（5秒）
                    WebDriverWait(thread_driver, 5).until(EC.presence_of_all_elements_located(
                        (By.ID, 'landingImage')))

                    # 画像URL
                    picture = thread_driver.find_element_by_id(
                        'landingImage').get_attribute('src')

                    # 商品名
                    product_name = thread_driver.find_element_by_id(
                        'productTitle').get_attribute('textContent').replace('\n', '')

                    # 価格
                    price = thread_driver.find_element_by_id(
                        'price').text

                    # 価格の不要行削除
                    if '\n' in price:
                        price = price[:price.find('\n')]
                    price = price[price.find('￥')+1:].replace(',', '')

                    # 価格の不要文字列削除
                    if ' ' in price:
                        price = price[:price.find(' ')]

                    # 評価
                    valuations = thread_driver.find_elements_by_class_name(
                        'a-icon-alt')
                    valuation = ''

                    for valuation in valuations:
                        if '星' in valuation.get_attribute('textContent'):
                            valuation = valuation.get_attribute(
                                'textContent')[-3:]
                        else:
                            valuation = "評価無し"

                    temp_products.append(
                        [product_name, price, valuation, picture, url])
                except:
                    self.logger.debug(url)
                    self.logger.debug(f'要素取得エラー：{traceback.format_exc()}')

            self.__products.extend(temp_products)

            self.logger.debug(f'詳細の取得完了：{len(temp_products)} 件')
        except:
            self.logger.debug(f'ページ情報取得エラー：{traceback.format_exc()}')

    # スレッドコントローラ
    def control_thread(self, urls):
        # スレッドに空きが出るまで待機
        while True:
            thread_list = threading.enumerate()
            thread_list.remove(threading.main_thread())

            runnable_thread_num = THREAD_NUM - len(thread_list)

            # 空きがあれば実行
            if runnable_thread_num > 0:
                thread = threading.Thread(
                    target=self.fetch_details_info, args=(urls,))
                thread.start()
                return

            time.sleep(0.5)

    # クローリング
    def fetch_products_data(self, keyword):

        self.logger.debug('#############START#############')

        # 時間計測用
        start_time = time.time()

        # amazonを開く
        self.driver.get(URL)

        # キーワードで検索実行
        self.driver.find_element_by_id(
            'twotabsearchtextbox').send_keys(keyword)
        self.driver.find_element_by_id('nav-search-submit-button').click()

        # 次へボタンがある間繰り返し
        while True:

            # 読み込み待機
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'a-last')))

            # 商品要素取得
            elements = self.driver.find_elements_by_class_name(
                'a-link-normal.s-no-outline')

            # url情報取得
            urls = []
            for element in elements:
                urls.append(element.get_attribute("href"))

            # スレッドコントローラ経由で商品情報の取得
            self.control_thread(urls)

            # 最終ページなら終了
            if self.driver.current_url[-2:] == '10':
                self.logger.debug('最終ページ')
                self.driver.close()
                break
            elif len(self.driver.find_elements_by_class_name('a-disabled.a-last')) > 0:
                self.logger.debug('最終ページ')
                self.driver.close()
                break

            # 次へボタンの要素取得
            a_last_elements = self.driver.find_elements_by_class_name('a-last')
            for element in a_last_elements:
                if element.text == '次へ→':
                    element.click()

        # すべてのスレッドの終了を待機
        thread_list = threading.enumerate()
        thread_list.remove(threading.main_thread())

        self.logger.debug(f'スレッド数：{len(thread_list)}')

        for thread in thread_list:
            thread.join()

        # 保存
        df = pd.DataFrame(self.__products)
        self.logger.debug(f'取得データ：{df}')
        df.columns = ['商品名', '価格', '評価', '画像URL', 'URL']
        df.to_excel('data.xlsx', index=None)

        # 完了フラグ

        # 処理時間算出
        elapsed_time = time.time() - start_time
        self.logger.debug(f'処理時間：{elapsed_time} sec')

        self.logger.debug('#############END#############')


# API利用
class AmazonApi():

    def __init__(self, driver: webdriver.Chrome):
        self.__keyword = ''
        self.__products = []  # 二次元 [ [商品名, 価格, 星, 画像URL, URL], ・・・ ]
        self.driver = driver
        self.__executed_flag = False

    @property
    def products(self):
        return self.__products

    @property
    def keyword(self):
        return self.__keyword

    @keyword.setter
    def keyword(self, keyword):
        self.__keyword = keyword

    @property
    def executed_flag(self):
        return self.__executed_flag
