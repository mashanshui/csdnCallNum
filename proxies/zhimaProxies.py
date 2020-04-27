# encoding: utf-8
# coding: utf-8
import random
import requests
from bs4 import BeautifulSoup
from lxml import etree


class Proxies:
    def __init__(self):
        self.home_url = 'http://http.tiqu.alicdns.com/getip3?num={}&type=2&pro=0&city=0&yys=0&port=11&pack=93717&ts=1&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions=&gm=4'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
        pass

    def getProxiesIpList(self, count, isHttps):
        url = self.home_url.format(count)
        web_data = requests.get(url)
        json = web_data.json()
        if json['code'] != 0:
            return []
        data = json['data']
        return data

    def getRandomProxiesIpList(self, count, isHttps):
        return self.getProxiesIpList(count, isHttps)


if __name__ == '__main__':
    ps = Proxies()
    ipList = ps.getProxiesIpList(2, 1)
    print(ipList)
