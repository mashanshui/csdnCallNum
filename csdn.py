# encoding: utf-8
# coding: utf-8
import os
import ssl
import time
import datetime
import random

from selenium.common.exceptions import TimeoutException

from proxies.proxiesUtil import Proxies
import logging
import configparser
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from selenium import webdriver
from config import articleIds, CALL_NUM

job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
schedulerBack = BackgroundScheduler(job_defaults=job_defaults)
schedulerBlock = BlockingScheduler(job_defaults=job_defaults)
job1 = None
job2 = None
job3 = None

config = configparser.ConfigParser()
config.read("config.ini")

logging.basicConfig(format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    filename='log', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

ssl._create_default_https_context = ssl._create_unverified_context


class CallCSDN(object):
    proxiesObject = Proxies()

    def __init__(self):
        self.url_home = "https://blog.csdn.net/shanshui911587154/article/details/{}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'blog.csdn.net',
            # 'Cookie':'uuid_tt_dd=10_18808468230-1574402025680-173534; dc_session_id=10_1574402025680.971581; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_18808468230-1574402025680-173534; __yadk_uid=iN17Q2d0dcnCLCMFdZkbJvV7SQnCQVDC; __gads=ID=52c67f757a0d6ccb:T=1582613877:S=ALNI_Mb3HuW4pc1ybWb4eB5vBibXe57ieg; UM_distinctid=1707b71e09827e-08d4e016f350c9-7a1b34-1fa400-1707b71e099155; CNZZDATA1258866300=1879187152-1582618416-https%253A%252F%252Fwww.baidu.com%252F%7C1582618416; Hm_lvt_e5ef47b9f471504959267fd614d579cd=1583224104; Hm_ct_e5ef47b9f471504959267fd614d579cd=6525*1*10_18808468230-1574402025680-173534; dc_sid=b7d9df0b9c846c335ebde25ec7019602; TY_SESSION_ID=8be5ed49-bf12-4b83-8afd-8b45eff2c896; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1585288181,1585290155,1585550648,1585892356; c-toolbar-writeguide=1; dc_tos=q87fiy; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1585904218; c-login-auto=13; announcement=%257B%2522isLogin%2522%253Afalse%252C%2522announcementUrl%2522%253A%2522https%253A%252F%252Fblog.csdn.net%252Fblogdevteam%252Farticle%252Fdetails%252F105203745%2522%252C%2522announcementCount%2522%253A0%252C%2522announcementExpire%2522%253A3600000%257D'
        }
        pass

    def run(self):
        url_list = self.getUrlList()
        print(url_list)
        i = 0
        for url in url_list:
            i = i + 1
            proxiesIp = self.proxiesObject.getRandomProxiesIpFromCache()
            driver = self.getDriverByProxy(proxiesIp)
            try:
                driver.get(url)
            except TimeoutException:
                # 当页面加载时间超过设定时间，通过js来stop，即可执行后续动作
                driver.execute_script("window.stop()")

            driver.save_screenshot(self.getImagePath(url))
            print('request {} by {} success'.format(url, proxiesIp))
            logging.info('request {} by {} success'.format(url, proxiesIp))
            self.saveCache()
            if (i < len(url_list)):
                time.sleep(random.randint(50, 80))
            driver.quit()
        pass

    def getImagePath(self, url):
        screen_path = os.path.abspath('screen_image')
        screen_file = os.path.join(screen_path,
                                   datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '_' +
                                   url.split('/')[6] + '.png')
        return screen_file

    def saveCache(self):
        today = config.getint("DEFAULT", "CALL_NUM_TODAY")
        total = config.getint("DEFAULT", "CALL_NUM_TOTAL")
        config.set("DEFAULT", "CALL_NUM_TODAY", str(today + 1))
        config.set("DEFAULT", "CALL_NUM_TOTAL", str(total + 1))
        config.write(open('config.ini', "w"))

    def getUrlList(self):
        url_list = []
        random.shuffle(articleIds)
        article_list = articleIds[0:random.randint(1, 4)]
        for articleId in article_list:
            url = self.url_home.format(articleId)
            url_list.append(url)
        return url_list

    def getDriverByProxy(self, proxiesIp):
        # 谷歌chrome
        # chromeOptions = webdriver.ChromeOptions()
        # chromeOptions.add_argument('headless')
        # chromeOptions.add_argument('--no-sandbox')
        # chromeOptions.add_argument('--proxy-server={}'.format(proxyIp))
        # driver = webdriver.Chrome(options=chromeOptions)
        # 火狐firefox
        fireProfile = webdriver.FirefoxProfile()
        if proxiesIp != None:
            ip = proxiesIp[0:proxiesIp.index(':', 6)]
            port = proxiesIp[proxiesIp.index(':', 6) + 1:]
            fireProfile.set_preference('network.proxy.type', 1)
            fireProfile.set_preference('network.proxy.http', ip)
            fireProfile.set_preference('network.proxy.http_port', int(port))
            fireProfile.set_preference('network.proxy.ssl', ip)
            fireProfile.set_preference('network.proxy.ssl_port', int(port))
            fireProfile.update_preferences()
        fireOptions = webdriver.FirefoxOptions()
        fireOptions.add_argument('-headless')
        driver = webdriver.Firefox(firefox_profile=fireProfile, options=fireOptions)
        driver.set_page_load_timeout(20)
        driver.set_script_timeout(20)
        return driver


def job_function1():
    print('执行任务一')
    config.set("DEFAULT", "CALL_NUM_TODAY", str(0))
    global job2
    if (job2 != None):
        schedulerBlock.remove_job(job2.id)
        job2 = None
    ms = CallCSDN()
    job2 = schedulerBlock.add_job(job_function2, 'interval', minutes=8, jitter=120, args=[ms])
    pass


def job_function2(callCsdnObject):
    print('执行任务二')
    callCsdnObject.run()
    today = config.getint("DEFAULT", "CALL_NUM_TODAY")
    if (today >= CALL_NUM):
        global job2
        schedulerBlock.remove_job(job2.id)
        job2 = None
        logging.info("访问量超过每天的限定值{}停止任务".format(CALL_NUM))
    pass


def job_function3():
    print('执行任务三')
    global job2
    if (job2 != None):
        schedulerBlock.remove_job(job2.id)
        job2 = None
    pass


# nohup python3 -u csdn.py > run.log 2>&1 &
if __name__ == '__main__':
    # https://www.cnblogs.com/tjp40922/p/10692476.html CenterOs装Python(CenterOs中默认是自带的python2)
    # 每天早上十点重新启动一次
    # 运行时间在早上10点到晚上10点之间(如果超过当日限定访问量会提前终止)
    # 每隔5到10分钟开启一次任务
    job3 = schedulerBack.add_job(job_function3, "cron", day='*', hour=22, minute=10)
    schedulerBack.start()
    job1 = schedulerBlock.add_job(job_function1, 'cron', day='*', hour=10, minute=10)
    schedulerBlock.start()
