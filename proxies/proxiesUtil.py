# encoding: utf-8
# coding: utf-8
from datetime import datetime

from proxies.xiciProxies import Proxies as xiciProxies
from proxies.zhimaProxies import Proxies as zhimaProxies
from config import UserProxy, ProxyType
import random

xici = 1
zhima = 2


class Proxies:
    proxiesObject = None
    xiciProxiesCacheList = []
    zhimaProxiesCacheList = []

    def __init__(self):
        self.type = ProxyType
        if ProxyType == xici:
            self.proxiesObject = xiciProxies()
        elif ProxyType == zhima:
            self.proxiesObject = zhimaProxies()
        pass

    def getProxiesIpList(self, count, isHttps):
        return self.proxiesObject.getProxiesIpList(count, isHttps)

    def getRandomProxiesIpList(self, count, isHttps):
        return self.proxiesObject.getRandomProxiesIpList(count, isHttps)

    def getRandomProxiesIpFromCache(self):
        if self.type == xici:
            return self.getRandomProxiesIpFromXici()
        elif self.type == zhima:
            return self.getRandomProxiesIpFromZhima()

    def getRandomIp(self, proxies):
        return random.choice(proxies)

    def getRandomProxiesIpFromXici(self):
        if UserProxy == 0:
            return None
        if len(self.xiciProxiesCacheList) == 0:
            self.xiciProxiesCacheList = list(self.getRandomProxiesIpList(5, 1))
        return self.getRandomIp(self.xiciProxiesCacheList)

    def getRandomProxiesIpFromZhima(self):
        if UserProxy == 0:
            return None
        if len(self.zhimaProxiesCacheList) == 0:
            self.zhimaProxiesCacheList = list(self.getRandomProxiesIpList(5, 1))
            if self.zhimaProxiesCacheList == None:
                return None
        for ips in self.zhimaProxiesCacheList:
            randomIp = self.getRandomIp(self.zhimaProxiesCacheList)
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if time > randomIp['expire_time']:
                self.zhimaProxiesCacheList.remove(randomIp)
            else:
                return str(randomIp['ip']) + ":" + str(randomIp['port'])
        return None


if __name__ == '__main__':
    ps = Proxies()
    ipList = ps.getRandomProxiesIpFromCache()
    print(ipList)
