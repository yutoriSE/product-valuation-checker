import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as bs4


class Sakura():

    def __init__(self, driver: webdriver):
        self.__valuations = []  # 二次元 [ [商品名, 価格, 星, サクラ星, サクラ度, URL, 画像URL], ・・・ ]
        self.driver = driver
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

    # 商品情報をスクレイピング

    def fetch_producs_valuation(self, products, keyword):
        self.__keyword = keyword
        self.__executed_flag = True
