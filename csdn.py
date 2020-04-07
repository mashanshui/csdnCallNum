import requests
import ssl
import time
import random
from proxiesUtil import Proxies
import logging
import configparser
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
# scheduler = BackgroundScheduler(job_defaults=job_defaults)
scheduler = BlockingScheduler(job_defaults=job_defaults)
job1 = None
job2 = None

config = configparser.ConfigParser()
config.read("config.ini")

logging.basicConfig(format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    filename='log', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

ssl._create_default_https_context = ssl._create_unverified_context
# 文章id
articleIds = [
    '54948224', '105194108', '105048964', '104820919', '104845505', '90290535', '88558209', '88395425', '86623646',
    '85229813', '85115340', '84635193', '82689963', '82288035', '81542638', '78719189', '78707486', '77461285',
    '74989779', '72500786', '55049627', '55046530'
]

# 代理ip，动态获取
proxies = [

]
# 日访问量
CALL_NUM = 100


class CallCSDN(object):
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
        global proxies
        proxies = Proxies().getRandomProxiesIpList(40)
        pass

    def run(self):
        url_list = self.getUrlList()
        print(url_list)
        i = 0
        for url in url_list:
            i = i + 1
            proxiesIp = 'http://{}'.format(self.getRandomIp())
            proxies = {'http': proxiesIp}
            rs = requests.get(url, headers=self.headers, proxies=proxies)
            if (rs.status_code == 200):
                print('request {} by {} success'.format(url, proxiesIp))
                logging.info('request {} by {} success'.format(url, proxiesIp))
                today = config.getint("DEFAULT", "CALL_NUM_TODAY")
                total = config.getint("DEFAULT", "CALL_NUM_TOTAL")
                config.set("DEFAULT", "CALL_NUM_TODAY", str(today + 1))
                config.set("DEFAULT", "CALL_NUM_TOTAL", str(total + 1))
                config.write(open('config.ini', "w"))
            else:
                print('request {} by {} fail'.format(url, proxiesIp))
                logging.error('request {} by {} fail'.format(url, proxiesIp))
            if (i < len(url_list)):
                time.sleep(random.randint(60, 100))
        pass

    def getUrlList(self):
        url_list = []
        random.shuffle(articleIds)
        article_list = articleIds[0:random.randint(1, 4)]
        for articleId in article_list:
            url = self.url_home.format(articleId)
            url_list.append(url)
        return url_list

    def getRandomIp(self):
        return random.choice(proxies)


def job_function1():
    print('执行任务一')
    global job2
    if (job2 != None):
        scheduler.remove_job(job2.id)
        job2 = None
    ms = CallCSDN()
    job2 = scheduler.add_job(job_function2, 'interval', minutes=8, jitter=120, args=[ms])
    pass


def job_function2(callCsdnObject):
    print('执行任务二')
    callCsdnObject.run()
    today = config.getint("DEFAULT", "CALL_NUM_TODAY")
    global CALL_NUM
    if (today >= CALL_NUM):
        global job2
        scheduler.remove_job(job2.id)
        logging.info("访问量超过每天的限定值{}停止任务".format(CALL_NUM))
    pass


if __name__ == '__main__':
    # 每天早上十点重新启动一次
    # 运行时间在早上10点到晚上6点之间
    # 每隔5到10分钟开启一次任务
    job1 = scheduler.add_job(job_function1, 'cron', day='*', hour=15, minute=45)
    scheduler.start()
    # while (True):
    #     time.sleep(1)
