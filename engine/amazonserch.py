import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as bs4


class Amazon():

    def __init__(self, driver: webdriver):
        self.__keyword = ''
        self.__products = []  # 二次元 [ [商品名, 価格, 星, URL, 画像URL], ・・・ ]
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

    # 在庫状況を取得

    def fetch_stock_status(self):
        pass

    # 商品情報を取得

    def fetch_product_data(self, url):
        pass
