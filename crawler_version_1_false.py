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

class JdSpider(object):
    def __init__(self):
        self.url='https://www.bilibili.com/v/music/vocaloid/#/all/default/1/'
        self.options=EdgeOptions() 
        self.options.use_chromium=True
        self.options.add_argument('headless')
        self.browser=webdriver.Edge() 
        self.i=0  
        self.page=1
        self.browser1=webdriver.Edge()
        self.browser2=webdriver.Edge()
        self.f=open("video.csv","w", encoding="utf-8")
        self.g=open("upspace.csv","w", encoding="utf-8")
        #self.db = pymysql.connect(host="localhost",user="root",password="18623275333lyf",database="mikufansdb")
        #self.cursor = self.db.cursor()

    def get_html(self):
        self.browser.get(self.url+str(self.page))

    def get_data(self):
        time.sleep(1)

        li_list=self.browser.find_elements_by_xpath('//*[@class="vd-list-cnt"]/ul/li')
        
        for li in li_list:
            item={}
            ActionChains(self.browser).move_to_element(li.find_element_by_xpath('.//div[@class="r"]/a')).perform()  
            item['name']=li.find_element_by_xpath('.//div[@class="r"]/a').text.strip().replace(",","，")
            self.f.write(item['name']+',')
            item['url']=li.find_element_by_xpath('.//div[@class="spread-module"]/a').get_attribute("href").strip()
            self.f.write(item['url']+',')
            item['picurl']=li.find_element_by_xpath('.//div[@class="lazy-img"]/img').get_attribute("src").strip()
            self.f.write(item['picurl']+',')
            item['intro']=li.find_element_by_xpath('.//div[@class="v-desc"]').text.strip().replace("\n"," ").replace(",","，")
            self.f.write(item['intro']+',')
            item['count']=li.find_element_by_xpath('.//div[@class="v-info"]/span[@class="v-info-i"]/span').text.strip()
            self.f.write(item['count']+',')
            item['uper']=li.find_element_by_xpath('.//div[@class="up-info"]').text.strip().replace(",","，")
            self.f.write(item['uper']+',')
            self.g.write(item['uper']+',')
            upspace=li.find_element_by_xpath('.//div[@class="up-info"]/a').get_attribute("href").strip()
            item['upspace']=upspace
            m = re.search("[^0-9]*?([0-9]+)",upspace)
            item['upid']=m.group(1)
            self.f.write(item['upid']+',')
            self.g.write(item['upid']+',')

            self.browser2.get(upspace)
            time.sleep(0.5)
            item['photourl']=self.browser2.find_element_by_xpath('//*[@class="h-avatar"]/img[@id="h-avatar"]').get_attribute("src").strip()
            self.g.write(item['photourl']+',')
            item['resume']=self.browser2.find_element_by_xpath('//*[@class="h-basic-spacing"]/h4').text.strip().replace("\n","").replace(",","，")
            self.g.write(item['resume']+',')
            item['fannum']=self.browser2.find_element_by_xpath('//*[@class="n-statistics"]/a[@class="n-data n-fs"]/p[@id="n-fs"]').text.strip()
            self.g.write(item['fannum']+'\n')

            self.browser1.get(item['url'])
            time.sleep(0.3)
            item['time']=self.browser1.find_element_by_xpath('//*[@class="video-data"]/span[3]').text.strip()
            self.f.write(item['name']+',')
            item['zan']=self.browser1.find_element_by_xpath('//*[@class="like"]').text.strip()
            if(item['zan']=='点赞'):
                item['zan']='0'
            item['bi']=self.browser1.find_element_by_xpath('//*[@class="coin"]').text.strip()
            if(item['bi']=='投币'):
                item['bi']='0'
            item['cang']=self.browser1.find_element_by_xpath('//*[@class="collect"]').text.strip()
            if(item['cang']=='收藏'):
                item['cang']='0'
            self.f.write(item['zan']+',')
            self.f.write(item['bi']+',')
            self.f.write(item['cang']+',')
            ActionChains(self.browser1).move_to_element(self.browser1.find_element_by_xpath('//a[@id="right-bottom-banner"]')).perform()
            time.sleep(0.3)
            item['comment_num'] = self.browser1.find_element_by_xpath('//div[@class="b-head"]/span[1]').text.strip()
            com_list=self.browser1.find_elements_by_xpath('//*[@class="comment-list "]/div')
            item['comment_1']='0'
            item['comment_2']='0'
            item['comment_3']='0'
            item['comment_4']='0'
            item['comment_5']='0'
            item['comment_number'] = '0'
            com_con = 1
            for com in com_list:
                if(item['comment_num'] == '0'):
                    item['comment_number'] = '0'
                    break
                if(item['comment_num'] == ''):
                    item['comment_number'] = '0'
                    break
                if(item['comment_num'] == ' '):
                    item['comment_number'] = '0'
                    break
                item['comment_'+str(com_con)]=com.find_element_by_xpath('.//p[@class="text"]').text.strip().replace("\n","").replace(",","，")
                item['comment_number'] = str(com_con)
                com_con+=1
                if com_con > 5:
                    break
            for i in range(1,6):
                self.f.write(item['comment_'+str(i)]+',')
            self.f.write(item['comment_number']+'\n')
            print(item)
            #sql = '''insert into mikufansdb.index_Video(name,intro,url,picurl,count,time,zan,bi,cang,uper,upid,comment_num,comment_1,comment_2,comment_3,comment_4,comment_5)
             #values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''' 
            #self.cursor.execute(sql, (item['name'], 
                #item['intro'], item['url'], item['picurl'], item['count'], item['time'], item['zan'], item['bi'], item['cang'],
                #item['uper'], item['upid'], item['comment_number'], item['comment_1'],item['comment_2'],item['comment_3'],item['comment_4'],item['comment_5']))
            #self.db.commit()
            #sql2='''insert into mikufansdb.index_Upspace(uper,upid,photourl,resume,fannum)
             #values(%s,%s,%s,%s,%s)'''
            #self.cursor.execute(sql2, (item['uper'],item['upid'],item['photourl'],item['resume'],item['fannum']))
            #self.db.commit()
            self.i+=1
            print("-----------------%d--------------"% ( self.i ) )

    def run(self):
        self.get_html()
        while True:
            self.get_data()
            if self.i >= 20:
                break
            if True:
                self.page+=1
                self.browser.get(self.url+str(self.page))
        #self.db.close()
        #self.cursor.close()
        self.f.close()
        self.g.close()




if __name__ == '__main__':
    spider=JdSpider()
    spider.run()
