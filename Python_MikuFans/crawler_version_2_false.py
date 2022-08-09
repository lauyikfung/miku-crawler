#coding:utf8
from pymysql.converters import convert_datetime
from pymysql.cursors import Cursor
from selenium import webdriver
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
from selenium.webdriver.common.action_chains import ActionChains
import time
import pymongo
import re
import pymysql
import requests
import pandas as pd
import random
import json
from ua_info import ua_list

class JdSpider(object):
    def __init__(self):
        self.url='https://www.bilibili.com/v/game/board/#/all/default/1/'
        #self.options=webdriver.FirefoxOptions()
        #self.options.add_argument('headless')#无界面浏览
        #self.browser=webdriver.Firefox(options=self.options)
        self.options=EdgeOptions() 
        self.options.use_chromium=True
        self.options.add_argument('headless')
        self.browser=webdriver.Edge() 
        self.i=0  
        self.page=1
        self.aid_list=[]
        self.mid_list=[]

    def get_html(self):
        self.browser.get(self.url+str(self.page))

    def get_data(self):
        time.sleep(2)

        li_list=self.browser.find_elements_by_xpath('//*[@class="vd-list-cnt"]/ul/li')
        for li in li_list:
            item={}
            ActionChains(self.browser).move_to_element(li.find_element_by_xpath('.//div[@class="r"]/a')).perform()  
            item['url']=li.find_element_by_xpath('.//div[@class="spread-module"]/a').get_attribute("href").strip()
            m = re.search("https://www\.bilibili\.com/video/BV(\w+)",item['url'])
            item['bvid']=m.group(1)

            url = 'https://api.bilibili.com/x/web-interface/view?bvid='+item['bvid']
            headers = {'User-Agent':random.choice(ua_list)}
            response = requests.get(url, headers=headers).json()
            item['aid']=str(response['data']['aid'])
            item['pic']=response['data']['pic'].strip()#视频封面
            item['title']=response['data']['title'].strip().replace(",","，")
            item['pubdate']=str(response['data']['pubdate'])
            item['desc']=response['data']['desc'].strip().replace("\n","").replace(",","，")#视频简介
            item['name']=response['data']['owner']['name'].strip().replace(",","，")#up主
            item['face']=response['data']['owner']['face'].strip()#up主
            item['mid']=str(response['data']['owner']['mid'])#up主
            item['view']=str(response['data']['stat']['view']).replace(",","")#播放量
            item['reply']=str(response['data']['stat']['reply']).replace(",","")
            item['favorite']=str(response['data']['stat']['favorite']).replace(",","")#收藏
            item['coin']=str(response['data']['stat']['coin']).replace(",","")#投币
            item['like']=str(response['data']['stat']['like']).strip().replace(",","")#点赞
            time.sleep(random.uniform(0.1, 0.5))
            url = 'https://api.bilibili.com/x/v2/reply/main?type=1&oid='+item['aid']
            headers = {'User-Agent':random.choice(ua_list)}
            response = requests.get(url, headers=headers).json()
            reply_n = 1
            if(item['reply']!='0'):
                for reply in response['data']['replies']:
                    dict = {}
                    dict['data'] = reply['content']['message'].strip().replace("\n","").replace(",","，")
                    item['comment'+str(reply_n)]=dict['data']
                    reply_n+=1
                if(reply_n>5):
                    break
            if(reply_n<=5):
                for n in range(reply_n,6):
                    item['comment'+str(n)]='0'
            time.sleep(random.uniform(0.1, 0.5))
            url = 'http://api.bilibili.com/x/relation/stat?vmid='+item['mid']
            headers = {'User-Agent':random.choice(ua_list)}
            response = requests.get(url, headers=headers).json()
            item['upfollower']=str(response['data']['follower']).replace(",","")
            time.sleep(random.uniform(0.1, 0.5))
            url = 'http://api.bilibili.com/x/space/acc/info?mid='+item['mid']
            headers = {'User-Agent':random.choice(ua_list)}
            response = requests.get(url, headers=headers).json()
            item['upname']=response['data']['name'].strip().replace(",","，")
            item['upface']=response['data']['face'].strip()#头像url
            item['upsign']=response['data']['sign'].strip().replace("\n","").replace(",","，")#up简介
            self.i+=1
            print(item)
            if(self.aid_list.count(item['aid']) == 0):
                self.aid_list.append(item['aid'])
            if(self.mid_list.count(item['mid']) == 0):
                self.mid_list.append(item['mid'])
            print("-----------------%d--------------"% ( self.i ) )
            time.sleep(0.1)

    def run(self):
        self.get_html()
        while True:
            self.get_data()
            if self.i >= 200:
                break
            if True:
                self.page+=1
                self.browser.get(self.url+str(self.page))
            print(self.mid_list)
            print(self.aid_list)
        self.browser.quit()
        




if __name__ == '__main__':
    spider=JdSpider()
    spider.run()
