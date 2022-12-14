import json
videof=open(r'D:\python-crawler\video.json','r',encoding='utf-8')
upspacef=open(r'D:\python-crawler\upspace.json','r',encoding='utf-8')
aidf=open(r'D:\python-crawler\aid.json','r',encoding='utf-8')
midf=open(r'D:\python-crawler\mid.json','r',encoding='utf-8')
new_videof=open(r'D:\python-crawler\video_new.json','w',encoding='utf-8')
new_upspacef=open(r'D:\python-crawler\upspace_new.json','w',encoding='utf-8')
old_v=json.load(videof)
old_u=json.load(upspacef)
aid_list=json.load(aidf)
mid_list=json.load(midf)
new_v=[]
new_u=[]
upnamef=open(r'D:\python-crawler\upname.json','w',encoding='utf-8')
upsignf=open(r'D:\python-crawler\upsign.json','w',encoding='utf-8')
titlef=open(r'D:\python-crawler\video_title.json','w',encoding='utf-8')
descf=open(r'D:\python-crawler\video_desc.json','w',encoding='utf-8')
upname_list=[]
upsign_list=[]
video_title_list=[]
video_desc_list=[]
for upmid in mid_list:
  upname_list.append(old_u[upmid]['upname'])
  upsign_list.append(old_u[upmid]['upsign'])
for aid in aid_list:
  video_title_list.append(old_v[aid]['title'])
  video_desc_list.append(old_v[aid]['desc'])
json.dump(upname_list,upnamef,ensure_ascii=False)
json.dump(upsign_list,upsignf,ensure_ascii=False)
json.dump(video_title_list,titlef,ensure_ascii=False)
json.dump(video_desc_list,descf,ensure_ascii=False)
upnamef.close()
upsignf.close()
titlef.close()
descf.close()
ord=0
for upmid in mid_list:
  item={}
  item['ord']=ord
  item['upface']="face/"+str(ord)+".jpg"
  item['mid']=old_u[upmid]['mid']
  item['upfollower']=old_u[upmid]['upfollower']
  item['upname']=old_u[upmid]['upname']
  item['upsign']=old_u[upmid]['upsign']
  item['video_num']=old_u[upmid]['video_num']
  tmp=[]
  for video in old_u[upmid]['upvideo']:
    tmp1={}
    tmp1['video_id']=aid_list.index(video)
    tmp1['video_photo']="video_photo/"+str(tmp1['video_id'])+".jpg"
    tmp1['video_title']=old_v[video]['title']
    tmp.append(tmp1)
  item['upvideo']=tmp
  new_u.append(item)
  ord+=1
ord=0
for aid in aid_list:
  item={}
  item['url']=old_v[aid]['url']
  item['ord']=ord
  item['pic']='video_photo/'+str(ord)+".jpg"
  item['title']=old_v[aid]['title']
  item['pubdate']=old_v[aid]['pubdate']
  item['desc']=old_v[aid]['desc']
  item['upname']=old_v[aid]['name']
  item['upmid']=old_v[aid]['mid']
  item['upord']=mid_list.index(item['upmid'])
  item['upface']="face/"+str(item['upord'])+".jpg"
  item['view']=old_v[aid]['view']
  item['favorite']=old_v[aid]['favorite']
  item['coin']=old_v[aid]['coin']
  item['like']=old_v[aid]['like']
  item['reply']=old_v[aid]['reply']
  tmp=[]
  for i in range(1,6):
    tmp.append(old_v[aid]['comment'+str(i)])
  item['comments']=tmp
  new_v.append(item)
  ord+=1
json.dump(new_u,new_upspacef,ensure_ascii=False)
json.dump(new_v,new_videof,ensure_ascii=False)
new_upspacef.close()
new_videof.close()
videof.close()
upspacef.close()
aidf.close()
midf.close()