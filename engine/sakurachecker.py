from engine.amazonserch import THREAD_NUM
from logging import Logger, debug
import pandas as pd
import threading
import traceback
import time
import os
import sys
from more_itertools import chunked
from webdriver_manager import driver, logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs4
from common import driver_generator

SAKURA_CHECKER_URL = 'https://sakura-checker.jp/'
THREAD_NUM = 10


class Sakura():

    def __init__(self, logger: Logger):
        self.__valuations = []
        self.__executed_flag = False
        self.__keyword = ''

    @property
    def valuations(self):
        return self.__valuations

    @property
    def keyword(self):
        return self.__keyword

    @keyword.setter
    def keyword(self, keyword):
        self.__keyword = keyword

    @property
    def executed_flag(self):
        return self.__executed_flag



    #商品の評価情報取得
    def fetch_valuation_details(self, products):
        chrome = driver_generator.set_driver(test_flag=False)
        temp_valuations = []
        
        #サクラチェック
        for product in products:

            #Amazonの商品ページurl
            url = product[4]

            chrome.get(SAKURA_CHECKER_URL)

            # 読み込み待機
            WebDriverWait(chrome, 10).until(EC.presence_of_all_elements_located((By.ID, 'urlsearchForm')))

            # 検索実行
            chrome.find_element_by_id('urlsearchForm').send_keys(url)

            # 読み込み待機
            WebDriverWait(chrome, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'item-rating')))

            #星
            star = chrome.find_element_by_class_name('item-rating').text

            #サクラ度
            sakura_rating = chrome.find_element_by_class_name('sakura-num').text

            #サクラチェックURL
            sakura_url = chrome.current_url

            temp_valuations = [star, sakura_rating, sakura_url]
        
        self.__valuations.append[temp_valuations]

        pass


    # ExcelシートからURLを読み込み、評価情報の取得
    def fetch_producs_valuation(self, products, keyword):
        self.__keyword = keyword
        self.__executed_flag = True

        #商品情報リストをスレッドの数に分割
        chunked_products = list(chunked(products, THREAD_NUM))

        #スレッド実行
        for cp in chunked_products:
            thread = threading.Thread(target=self.fetch_valuation_details, args=(cp, ))
            thread.start()

        # すべてのスレッドの終了を待機
        thread_list = threading.enumerate()
        thread_list.remove(threading.main_thread())

        for thread in thread_list:
            thread.join()

        #Excelで出力
        df = pd.DataFrame(self.__valuations)
        df.columns = ["商品名", "価格", "サクラ度", "Amazon評価", "サクラチェッカー評価", "画像URL", "AmazonURL", "サクラチェッカーURL"]
        df.to_excel(keyword+'_valuations.xlsx', index=None)
