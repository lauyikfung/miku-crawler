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
import urllib.error
from ua_info_1 import ua_list

class MikuSpider(object):
    def __init__(self):
        self.page=1
        self.url='https://www.bilibili.com/v/music/vocaloid/#/all/default/0/'
        self.options=EdgeOptions() 
        self.options.use_chromium=True
        #self.options.add_argument('user-agent="%s"' % random.choice(ua_list))
        self.options.add_argument('headless')
        self.browser=webdriver.Edge() 
        self.i=0
        self.x=26
        self.banned = False
        self.browser_1=webdriver.Edge()
        self.browser_2=webdriver.Edge()
        self.browser_3=webdriver.Edge()
        self.browser_4=webdriver.Edge()  
        self.aid_list=[]
        self.mid_list=[]
        self.all_video={}
        self.all_upspace={}
        self.f=open(r'D:\python-crawler\video_'+str(self.x)+r'.json','w',encoding='utf-8')
        self.g=open(r'D:\python-crawler\upspace_'+str(self.x)+r'.json','w',encoding='utf-8')
        self.all_aid=open(r'D:\python-crawler\aid_'+str(self.x)+r'.json','w',encoding='utf-8')
        self.all_mid=open(r'D:\python-crawler\mid_'+str(self.x)+r'.json','w',encoding='utf-8')

    def get_html(self):
        self.browser.get(self.url+str(self.page))

    def get_data(self):
        time.sleep(2)

        li_list=self.browser.find_elements_by_xpath('//*[@class="vd-list-cnt"]/ul/li')
        for li in li_list:
            item={}
            video_info = {}
            upspace_info = {}
            ActionChains(self.browser).move_to_element(li.find_element_by_xpath('.//div[@class="r"]/a')).perform()  
            video_info['url']=item['url']=li.find_element_by_xpath('.//div[@class="spread-module"]/a').get_attribute("href").strip()
            m = re.search("https://www\.bilibili\.com/video/BV(\w+)",item['url'])
            video_info['bvid']=item['bvid']=m.group(1)
            time.sleep(random.uniform(0.3,0.5))
            url = 'https://api.bilibili.com/x/web-interface/view?bvid='+item['bvid']
            self.browser_1.get(url)
            if(self.browser_1.find_element_by_xpath('//pre').text == None):
                self.banned = True
                time.sleep(random.uniform(0.5, 1))
                return
            response = json.loads(self.browser_1.find_element_by_xpath('//pre').text)
            if(response['data'] == None):
                self.banned = True
                time.sleep(random.uniform(0.5, 1))
                return
            thisvideo=video_info['aid']=item['aid']=str(response['data']['aid'])
            video_info['pic']=response['data']['pic'].strip()#视频封面
            video_info['title']=item['title']=response['data']['title'].strip()
            local_time = time.localtime(response['data']['pubdate'])
            video_info['pubdate']=time.strftime("%Y-%m-%d %H:%M:%S", local_time)
            video_info['desc']=response['data']['desc'].strip()#视频简介
            video_info['name']=item['name']=response['data']['owner']['name'].strip()#up主
            video_info['face']=response['data']['owner']['face'].strip()#up主
            upspace_info['mid']=video_info['mid']=item['mid']=str(response['data']['owner']['mid'])#up主
            video_info['view']=str(response['data']['stat']['view'])#播放量
            video_info['favorite']=str(response['data']['stat']['favorite'])#收藏
            video_info['coin']=str(response['data']['stat']['coin'])#投币
            video_info['like']=str(response['data']['stat']['like']).strip()#点赞
            time.sleep(random.uniform(0.3,0.5))
            url = 'https://api.bilibili.com/x/v2/reply/main?type=1&oid='+item['aid']
            self.browser_2.get(url)
            if(self.browser_2.find_element_by_xpath('//pre').text == None):
                self.banned = True
                time.sleep(random.uniform(0.5, 1))
                return
            response = json.loads(self.browser_2.find_element_by_xpath('//pre').text)
            if(response['data'] == None):
                self.banned = True
                time.sleep(random.uniform(0.5, 1))
                return
            reply_n = 1
            if(response['data']['replies'] != None):
                for reply in response['data']['replies']:
                    dict = {}
                    dict['data'] = reply['content']['message'].strip()
                    video_info['comment'+str(reply_n)]=dict['data']
                    reply_n+=1
                    if(reply_n>5):
                        break
            if(reply_n<=5):
                for n in range(reply_n,6):
                    video_info['comment'+str(n)]='---'
            video_info['reply']=reply_n-1
            time.sleep(random.uniform(0.3,0.5))
            url = 'http://api.bilibili.com/x/relation/stat?vmid='+item['mid']
            self.browser_3.get(url)
            if(self.browser_3.find_element_by_xpath('//pre').text == None):
                self.banned = True
                time.sleep(random.uniform(0.5, 1))
                return
            response = json.loads(self.browser_3.find_element_by_xpath('//pre').text)
            if((response['code'] != 0) or (response['data'] == None)):
                self.banned = True
                time.sleep(random.uniform(0.5, 1))
                return
            upspace_info['upfollower']=str(response['data']['follower'])
            time.sleep(random.uniform(0.3,0.5))
            url = 'http://api.bilibili.com/x/space/acc/info?mid='+item['mid']
            self.browser_4.get(url)
            if(self.browser_4.find_element_by_xpath('//pre').text == None):
                self.banned = True
                time.sleep(random.uniform(0.5, 1))
                return
            response = json.loads(self.browser_4.find_element_by_xpath('//pre').text)
            if((response['code'] != 0) or (response['data'] == None)):
                self.banned = True
                time.sleep(random.uniform(0.5, 1))
                return
            upspace_info['upname']=response['data']['name'].strip()
            upspace_info['upface']=response['data']['face'].strip()#头像url
            upspace_info['upsign']=response['data']['sign'].strip()#up简介
            self.i+=1
            print(item)
            if((self.mid_list.count(item['mid']) != 0) and (self.aid_list.count(item['aid']) == 0)):
                new_upspace = {}
                new_upspace['mid']=self.all_upspace[item['mid']]['mid']
                new_upspace['upname']=self.all_upspace[item['mid']]['upname']
                new_upspace['upface']=self.all_upspace[item['mid']]['upface']
                new_upspace['upsign']=self.all_upspace[item['mid']]['upsign']
                new_upspace['upfollower']=self.all_upspace[item['mid']]['upfollower']
                new_upspace['video_num']=self.all_upspace[item['mid']]['video_num']+1
                upvideo=self.all_upspace[item['mid']]['upvideo']
                upvideo.append(thisvideo)
                new_upspace['upvideo']=upvideo
                self.all_upspace.update({item['mid']:new_upspace})
            if(self.aid_list.count(item['aid']) == 0):
                self.aid_list.append(item['aid'])
                self.all_video[item['aid']] = video_info
            if(self.mid_list.count(item['mid']) == 0):
                self.mid_list.append(item['mid'])
                upvideo=[]
                upvideo.append(thisvideo)
                upspace_info['upvideo']=upvideo
                upspace_info['video_num']=1
                self.all_upspace[item['mid']] = upspace_info
            print("-----------------%d--------------"% ( self.i ) )
            time.sleep(random.uniform(0.3,0.5))

    def run(self):
        self.get_html()
        while True:
            self.get_data()
            if self.i >= 1000:
                break
            if True:
                if self.banned == True:
                    print("banned!!!!!!!!!!!!!!!!")
                    print("banned!!!!!!!!!!!!!!!!")
                    print("banned!!!!!!!!!!!!!!!!")
                    print("banned!!!!!!!!!!!!!!!!")
                    print("banned!!!!!!!!!!!!!!!!")
                    break
                self.page+=1
                self.browser.get(self.url+str(self.page))
            if self.page % 10 == 1:
                json.dump(self.all_video,self.f,ensure_ascii=False)
                json.dump(self.all_upspace,self.g,ensure_ascii=False)
                self.f.close()
                self.g.close()
                json.dump(self.aid_list,self.all_aid,ensure_ascii=False)
                json.dump(self.mid_list,self.all_mid,ensure_ascii=False)
                self.all_aid.close()
                self.all_mid.close()
                self.x+=1
                self.aid_list=[]
                self.mid_list=[]
                self.all_video={}
                self.all_upspace={}
                self.f=open(r'D:\python-crawler\video_'+str(self.x)+r'.json','w',encoding='utf-8')
                self.g=open(r'D:\python-crawler\upspace_'+str(self.x)+r'.json','w',encoding='utf-8')
                self.all_aid=open(r'D:\python-crawler\aid_'+str(self.x)+r'.json','w',encoding='utf-8')
                self.all_mid=open(r'D:\python-crawler\mid_'+str(self.x)+r'.json','w',encoding='utf-8')
                self.browser_1.quit()
                self.browser_2.quit()
                self.browser_3.quit()
                self.browser_4.quit()
        json.dump(self.all_video,self.f,ensure_ascii=False)
        json.dump(self.all_upspace,self.g,ensure_ascii=False)
        self.f.close()
        self.g.close()
        json.dump(self.aid_list,self.all_aid,ensure_ascii=False)
        json.dump(self.mid_list,self.all_mid,ensure_ascii=False)
        self.all_aid.close()
        self.all_mid.close()
        self.browser.quit()

if __name__ == '__main__':
    spider=MikuSpider()
    spider.run()
