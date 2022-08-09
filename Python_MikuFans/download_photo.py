import json
import requests
from ua_info_1 import ua_list
import random
import time
aidf = open(r'D:\python-crawler\aid.json','r',encoding='utf-8')
midf = open(r'D:\python-crawler\mid.json','r',encoding='utf-8')
videof = open(r'D:\python-crawler\video.json','r',encoding='utf-8')
upspacef = open(r'D:\python-crawler\upspace.json','r',encoding='utf-8')
aid_all = json.load(aidf)
mid_all = json.load(midf)
video_all = json.load(videof)
upspace_all = json.load(upspacef)
face_pack = 'D:/python-crawler/face/'
video_photo_pack = 'D:/python-crawler/video_photo/'
face_i = 0
photo_i = 0
for aid in aid_all:
  url = video_all[aid]['pic']
  headers = {'User-Agent':random.choice(ua_list)}
  pic = requests.get(url=url, headers=headers).content
  filename = video_photo_pack+str(photo_i)+".jpg"
  with open(filename, "wb") as f:
    f.write(pic)
  photo_i+=1
  time.sleep(random.uniform(0.8, 1.2))
for mid in mid_all:
  url = upspace_all[mid]['upface']
  headers = {'User-Agent':random.choice(ua_list)}
  pic = requests.get(url=url, headers=headers).content
  filename = face_pack+str(face_i)+".jpg"
  with open(filename, "wb") as f:
    f.write(pic)
  face_i+=1
  time.sleep(random.uniform(0.8, 1.2))
aidf.close()
midf.close()
videof.close()
upspacef.close()