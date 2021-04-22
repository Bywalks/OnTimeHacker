#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

'''
Program：OnTimeHacker
Function：Get Src Notice OnTime
 
Version：Python3
Time：2021/4/15
Author：bywalks
Blog：http://www.bywalks.com
Github：https://github.com/bywalks
'''

import sys
import json
import time
from requests.packages import urllib3
import requests
from bs4 import BeautifulSoup

banner = '''
   ____     _______ _                _    _            _             
  / __ \   |__   __(_)              | |  | |          | |            
 | |  | |_ __ | |   _ _ __ ___   ___| |__| | __ _  ___| | _____ _ __ 
 | |  | | '_ \| |  | | '_ ` _ \ / _ |  __  |/ _` |/ __| |/ / _ | '__|
 | |__| | | | | |  | | | | | | |  __| |  | | (_| | (__|   |  __| |   
  \____/|_| |_|_|  |_|_| |_| |_|\___|_|  |_|\__,_|\___|_|\_\___|_|      
                                     By Bywalks | V 1.0  
                                     
[+]爬取各个SRC平台的公告通知
[+]对各大SRC当日推出公告进行推送到微信，结合系统定时任务可实现SRC平台公告监测
[+]目前支持的SRC平台[当前共计24家]：
360、爱奇艺、阿里、百度、哔哩哔哩、贝壳、Boss、58、菜鸟、滴滴、斗鱼、
饿了么、瓜子、合合、享道、京东、焦点、快手、美团、水滴、顺丰、腾讯、中通、字节                         
'''

urllib3.disable_warnings()

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

def Send_VX(src_name, src_title):
    notice = "[+]%s今日存在公告通知：%s" %(src_name,src_title)
    print(notice)
    requests.get('https://sc.ftqq.com/%s.send?text=%s&desp=%s' % (key,src_name,src_title))


def src_360():
    print("[+]开始监测360 SRC..")
    url = 'https://security.360.cn/News/news?type=-1'
    r = requests.get(url, headers=headers,timeout=5,verify=False)
    bs = BeautifulSoup(r.text, 'lxml')
    notice_list = bs.select('.news-content')[0].select('li')
    src_time = notice_list[4].select('.new-list-time')[0].text.strip()
    src_title = notice_list[4].select('a')[0].text
    if src_time == current_time:
        Send_VX("360",src_title)

def iqiyi():
    print("[+]开始监测爱奇艺 SRC..")
    url = 'https://security.iqiyi.com/api/publish/notice/list?sign=6ce5b4f7ad460b2ae3046422f61f905e4e3ecd03'
    r = requests.get(url,headers=headers,timeout=5,verify=False)
    r_json = json.loads(r.text)
    notice_list = r_json['data']
    src_time = notice_list[0]['create_time_str']
    src_title = notice_list[0]['title']
    if src_time == current_time:
       Send_VX('爱奇艺',src_title)
    
def alibaba():
    print("[+]开始监测阿里巴巴 SRC..")
    url = 'https://security.alibaba.com/api/asrc/pub/announcements/list.json?&page=1'
    r = requests.get(url,headers=headers,timeout=5,verify=False)
    r_json = json.loads(r.text)
    notice_list = r_json['data']['rows']
    src_time = notice_list[0]['lastModify'].split(' ')[0]
    src_title = notice_list[0]['title']
    if src_time == current_time:
        Send_VX('阿里',src_title)

def baidu():
    print("[+]开始监测百度 SRC..")
    url = 'https://bsrc.baidu.com/v2/api/announcement?type=&page=1&pageSize=10'
    r = requests.get(url,headers=headers,timeout=5,verify=False)
    r_json = json.loads(r.text)
    notice_list = r_json['retdata']['announcements']
    src_time = notice_list[0]['createTime'].split(' ')[0]
    src_title = notice_list[0]['title']
    if src_time == current_time:
        Send_VX('百度', src_title)

def bilibili():
    print("[+]开始监测哔哩哔哩 SRC..")
    url = 'https://security.bilibili.com/announcement/'
    r = requests.get(url,headers=headers,timeout=5,verify=False)
    bs = BeautifulSoup(r.text, 'lxml')
    notice_list = bs.select('td')
    src_time = notice_list[2].text.replace('\n', '')
    src_title = notice_list[3].text.replace('\n', '')
    if src_time == current_time:
        Send_VX('哔哩哔哩', src_title)
    
def ke():
    print("[+]开始监测贝壳 SRC..")
    url = 'https://security.ke.com/api/notices/list'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Referer': 'https://security.ke.com/notices'
}
    r = requests.post(url, headers=headers, data={"page": 1})
    r_json = json.loads(r.text)
    notice_list = r_json['data']['list']
    src_time = notice_list[0]['createTime'].split(' ')[0]
    src_title = notice_list[0]['title']
    if src_time == current_time:
        Send_VX('贝壳', src_title)
    
def boss():
    print("[+]开始监测Boss SRC..")
    url = 'https://src.zhipin.com/announcement'
    r = requests.get(url,headers=headers,timeout=5,verify=False)
    bs = BeautifulSoup(r.text, 'lxml')
    notice_list = bs.select('.announcement_list')[0].select('li')
    src_time = notice_list[0].select('.list_date')[0].text.strip()[0:4]+"-"+notice_list[0].select('.list_date')[0].text.strip()[5:7]+"-"+notice_list[0].select('.list_date')[0].text.strip()[8:10]
    src_title = notice_list[0].select('.list_title')[0].text
    if src_time == current_time:
        Send_VX('贝壳', src_title)

def src_58():
    print("[+]开始监测58 SRC..")
    url = 'https://security.58.com/notice/'
    r = requests.get(url,headers=headers,timeout=5,verify=False)
    bs = BeautifulSoup(r.text, 'lxml')
    notice_list = bs.select('.time')
    src_time = notice_list[0].text
    src_title = bs.select('.box')[0].select('a')[0].text
    if src_time == current_time:
        Send_VX('贝壳', src_title)
    
def cainiao():
    print("[+]开始监测菜鸟 SRC..")
    url = 'https://sec.cainiao.com/announcement.htm'
    r = requests.get(url,headers=headers,timeout=5,verify=False)
    bs = BeautifulSoup(r.text, 'lxml')
    notice_list = bs.select('td')
    src_time = notice_list[0].text.split('\n')[0].strip().split('][')[0].replace('[', '')
    src_title = notice_list[0].text.split('\n')[1].strip()
    if src_time == current_time:
        Send_VX('菜鸟', src_title)
        
def didi():
    print("[+]开始监测滴滴 SRC..")
    url = 'http://sec.didichuxing.com/rest/article/list?page=1&size=5&option=0'
    r = requests.get(url,headers=headers,timeout=5,verify=False)
    r_json = json.loads(r.text)
    notice_list = r_json['data']
    timeStamp = notice_list[0]['time']
    src_time = time.strftime("%Y-%m-%d", time.localtime(float(timeStamp / 1000)))
    src_title = notice_list[0]['title']
    if src_time == current_time:
        Send_VX('滴滴', src_title)

def douyu():
    print("[+]开始监测斗鱼 SRC..")
    url = 'https://security.douyu.com/api/v1/announcement_list?announcement_type=1&current=1&size=10'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Referer': 'https://security.douyu.com/'
}
    r = requests.get(url,headers=headers,timeout=5,verify=False)
    r_json = json.loads(r.text)
    notice_list = r_json['data']['records']
    src_time = notice_list[0]['publish_time']
    src_title = notice_list[0]['title']
    if src_time == current_time:
        Send_VX('斗鱼', src_title)   

def ele():
    print("[+]开始监测饿了么 SRC..")
    url = 'https://security.ele.me/api/bulletin/listBulletins?offset=0&limit=5'
    r = requests.get(url, headers=headers,timeout=5,verify=False)
    r_json = json.loads(r.text)
    notice_list = r_json['modelList']
    timeStamp = notice_list[0]['createdAt']
    src_time = time.strftime("%Y-%m-%d", time.localtime(float(timeStamp / 1000)))
    src_title = notice_list[0]['title']
    if src_time == current_time:
        Send_VX('饿了么', src_title)

def guazi():
    print("[+]开始监测瓜子 SRC..")
    url = 'https://security.guazi.com/gzsrc/notice/queryNoticesList'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
    r = requests.post(url, headers=headers, data="pageNo=1")
    r_json = json.loads(r.text)
    notice_list = r_json['data']['list']
    src_time = notice_list[0]['publishDate'].split(' ')[0]
    src_title = notice_list[0]['title']
    if src_time == current_time:
        Send_VX('瓜子', src_title)
    
def hehe():
    print("[+]开始监测合合 SRC..")
    url = 'https://security.intsig.com/index.php?m=&c=page&a=index'
    r = requests.get(url,headers=headers,timeout=5,verify=False)
    bs = BeautifulSoup(r.text, 'lxml')
    notice_list = bs.select('.announcement_list')[0].select('li')
    src_time = notice_list[0].select('.list_date')[0].text.strip()[0:4]+"-"+notice_list[0].select('.list_date')[0].text.strip()[5:7]+"-"+notice_list[0].select('.list_date')[0].text.strip()[8:10]
    src_title = notice_list[0].select('.list_title')[0].text
    if src_time == current_time:
        Send_VX('合合', src_title)    

def xiangdao():
    print("[+]开始监测享道 SRC..")
    url = 'https://src.saicmobility.com/news/'
    r = requests.get(url,headers=headers,timeout=5,verify=False)
    bs = BeautifulSoup(r.text, 'lxml')
    src_time = bs.select('.side')[0].select('.news-date')[0].text.strip()[0:4]+"-"+bs.select('.side')[0].select('.news-date')[0].text.strip()[5:6]+"-"+bs.select('.side')[0].select('.news-date')[0].text.strip()[7:9]
    src_title = bs.select('.side')[0].select('.news-title')[0].text
    if '-' in src_time[5:7]:
        src_time=src_time[0:5]+"0"+src_time[5:9]
    if src_time == current_time:
        Send_VX('享道', src_title)

def jd():
    print("[+]开始监测京东 SRC..")
    url = 'https://security.jd.com/notice/list?parent_type=2&child_type=0&offset=0&limit=12'
    r = requests.get(url,headers=headers,timeout=5,verify=False)
    r_json = json.loads(r.text)
    notice_list = r_json['data']['notices']
    src_time = notice_list[0]['CreateTime'].split(' ')[0]
    src_title = notice_list[0]['Title']
    if src_time == current_time:
        Send_VX('京东', src_title)

def jiaodian():
    print("[+]开始监测焦点 SRC..")
    url = 'https://security.focuschina.com/home/announcement.html'
    r = requests.get(url,headers=headers,timeout=5,verify=False)
    bs = BeautifulSoup(r.text, 'lxml')
    notice_list = bs.select('.content-bd')[0].select('li')
    src_time = notice_list[0].select('.anno-lst-date')[0].text.strip()
    src_title = notice_list[0].select('a')[0].text.strip()[16:36]
    if src_time == current_time:
        Send_VX('焦点', src_title)
    
def kuaishou():
    print("[+]开始监测快手 SRC..")
    url = 'https://security.kuaishou.com/rest/k/notice/list'
    headers = {
        'Referer': 'https://security.kuaishou.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
    r = requests.post(url, headers=headers, data="",timeout=5,verify=False)
    r_json = json.loads(r.text)
    notice_list = r_json['data']
    src_time = notice_list[0]['submitTime']
    src_title = notice_list[0]['title']
    if src_time == current_time:
        Send_VX('快手', src_title)    

def meituan():
    print("[+]开始监测美团 SRC..")
    url = 'https://security.meituan.com/api/announce/list?typeId=0&curPage=1&perPage=5'
    r = requests.get(url, headers=headers,timeout=5,verify=False)
    r_json = json.loads(r.text)
    notice_list = r_json['data']['items']
    timeStamp = notice_list[0]['createTime']
    src_time = time.strftime("%Y-%m-%d", time.localtime(float(timeStamp / 1000)))
    src_title = notice_list[0]['name']
    if src_time == current_time:
        Send_VX('美团', src_title)

def shuidi():
    print("[+]开始监测水滴 SRC..")
    url = 'https://api.shuidihuzhu.com/api/wide/announce/getAnnouncePageList'
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
    }
    r = requests.post(url, headers=headers, data='{"pageNum":1,"pageSize":10}',timeout=5,verify=False)
    r_json = json.loads(r.text)
    notice_list = r_json['data']['list']
    timeStamp = notice_list[0]['updateTime']
    src_time = time.strftime("%Y-%m-%d", time.localtime(float(timeStamp / 1000)))
    src_title = notice_list[0]['title']
    if src_time == current_time:
        Send_VX('水滴', src_title)

def shunfeng():
    print("[+]开始监测顺丰 SRC..")
    url = 'http://sfsrc.sf-express.com/notice/getLatestNotices'
    r = requests.post(url, headers=headers, data="limit=10&offset=0",timeout=5,verify=False)
    r_json = json.loads(r.text)
    notice_list = r_json['rows']
    timeStamp = notice_list[0]['modifyTime']
    src_time = time.strftime("%Y-%m-%d", time.localtime(float(timeStamp / 1000)))
    src_title = notice_list[0]['noticeTitle']
    if src_time == current_time:
        Send_VX('顺丰', src_title)

def tencent():
    print("[+]开始监测腾讯 SRC..")
    url = 'https://security.tencent.com/index.php/announcement'
    r = requests.get(url, headers=headers,timeout=5,verify=False)
    bs = BeautifulSoup(r.text, 'html.parser')
    notice_list = bs.select('.section-announcement')[0].select('li')
    src_time = notice_list[0].select('span')[0].text.replace('/', '-')
    src_title = notice_list[0].select('a')[0].text
    if src_time == current_time:
        Send_VX('腾讯', src_title)

def zto():
    print("[+]开始监测中通 SRC..")
    url = 'https://sec.zto.com/api/notice/list'
    r = requests.get(url, headers=headers,timeout=5,verify=False)
    r_json = json.loads(r.text)
    notice_list = r_json
    src_time = notice_list[0]['updated_at'].split('.')[0].replace('T', ' ').split(' ')[0]
    src_title = notice_list[0]['title']
    if src_time == current_time:
        Send_VX('中通', src_title)


def bytedance():
    print("[+]开始监测字节 SRC..")
    url = 'https://security.bytedance.com/notice/getNotices/'
    r = requests.get(url, headers=headers,timeout=5,verify=False)
    bs = BeautifulSoup(r.text, 'lxml')
    notice_list = bs.select('.container')[0].select('li')
    src_time = notice_list[0].select('span')[0].text.split(' ')[0].replace('年', '-').replace('月', '-').replace('日', '')
    if '-' in src_time[5:7]:
        src_time=src_time[0:5]+"0"+src_time[5:9]
    src_title = notice_list[0].select('a')[0].text
    if src_time == current_time:
        Send_VX('字节', src_title)

if __name__ == '__main__':
    print(banner)
    global key
    key = ''  # 填写上你 Server酱的 key，key 申请地址：http://sc.ftqq.com/
    number = 3
    if key == '':
        print('请在代码中填写上你 Server酱的 key，key 申请地址：http://sc.ftqq.com/')
        sys.exit()
    current_time = time.strftime("%Y-%m-%d", time.localtime())
    src_360()
    iqiyi()
    alibaba()
    baidu()
    bilibili()
    ke()
    boss()
    src_58()
    cainiao()
    didi()
    douyu()
    ele()
    guazi()
    hehe()
    xiangdao()
    jd()
    jiaodian()
    kuaishou()
    meituan()
    shuidi()
    shunfeng()
    tencent()
    zto()
    bytedance()
