# encoding: utf-8
# coding: utf-8
import random
import requests
from bs4 import BeautifulSoup
from lxml import etree


class Proxies:
    def __init__(self):
        self.home_url = 'http://www.xicidaili.com/wn/{}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
        pass

    def getProxiesIpList(self, count, isHttps):
        proxiesIpList = []
        for i in range(1, 20):
            url = self.home_url.format(i)
            web_data = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(web_data.text, 'lxml')
            ips = soup.find_all('tr')
            for i in range(1, len(ips)):
                ip_info = ips[i]
                tds = ip_info.find_all('td')  # tr标签中获取td标签数据
                if tds[8].text.find('天') != -1 and tds[4].text.find('高匿') != -1:
                    proxiesIpList.append(tds[1].text + ':' + tds[2].text)
                    if (len(proxiesIpList) >= count):
                        break
            if (len(proxiesIpList) >= count):
                break
        return proxiesIpList

    def getRandomProxiesIpList(self, count, isHttps):
        proxiesIpList = []
        randomNum = list(range(20))
        random.shuffle(randomNum)
        for i in randomNum:
            url = self.home_url.format(i)
            web_data = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(web_data.text, 'lxml')
            ips = soup.find_all('tr')
            for i in range(1, len(ips)):
                ip_info = ips[i]
                tds = ip_info.find_all('td')  # tr标签中获取td标签数据
                if not tds[8].text.find('天') == -1:
                    proxiesIpList.append(tds[1].text + ':' + tds[2].text)
                    if (len(proxiesIpList) >= count):
                        break
            if (len(proxiesIpList) >= count):
                break
        random.shuffle(proxiesIpList)
        return proxiesIpList


if __name__ == '__main__':
    ps = Proxies()
    ipList = ps.getRandomProxiesIpList(20,1)
    print(ipList)
