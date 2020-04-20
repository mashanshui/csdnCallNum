# encoding: utf-8
# coding: utf-8
from proxies.xiciProxies import Proxies as xiciProxies
from proxies.zhimaProxies import Proxies as zhimaProxies

xici = 0
zhima = 1


class Proxies:
    proxiesObject = None

    def __init__(self, type):
        self.type = type
        if type == xici:
            self.proxiesObject = xiciProxies()
        elif type == zhima:
            self.proxiesObject = zhimaProxies()
        pass

    def getProxiesIpList(self, count):
        return self.proxiesObject.getProxiesIpList(count)

    def getRandomProxiesIpList(self, count):
        return self.proxiesObject.getRandomProxiesIpList(count)


if __name__ == '__main__':
    ps = Proxies(zhima)
    ipList = ps.getRandomProxiesIpList(20)
    print(ipList)
