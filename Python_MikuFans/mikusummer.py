import json
summer = 0
sumup = 0
f = []
mid_26 = []
video_26 = []
upspace_26 = []
aid_all = []
mid_all = []
video_all = {}
upspace_all = {}
total_data = {}
aidf = open(r'D:\python-crawler\aid.json','w',encoding='utf-8')
midf = open(r'D:\python-crawler\mid.json','w',encoding='utf-8')
videof = open(r'D:\python-crawler\video.json','w',encoding='utf-8')
upspacef = open(r'D:\python-crawler\upspace.json','w',encoding='utf-8')
total_dataf = open(r'D:\python-crawler\total_data.json','w',encoding='utf-8')
for i in range(1, 27):
  f.append(open(r'D:\python-crawler\aid_'+str(i)+r'.json','r',encoding='utf-8'))
  mid_26.append(open(r'D:\python-crawler\mid_'+str(i)+r'.json','r',encoding='utf-8'))
  video_26.append(open(r'D:\python-crawler\video_'+str(i)+r'.json','r',encoding='utf-8'))
  upspace_26.append(open(r'D:\python-crawler\upspace_'+str(i)+r'.json','r',encoding='utf-8'))
  tmp_aid = json.load(f[i - 1])
  tmp_video = json.load(video_26[i - 1])
  for j in tmp_aid:
    if(aid_all.count(j)==0):
      summer+=1
      video_all[j]=tmp_video[j]
      aid_all.append(j)
for i in range(1, 27):
  tmp_mid = json.load(mid_26[i - 1])
  tmp_upspace = json.load(upspace_26[i - 1])
  for j in tmp_mid:
    if(mid_all.count(j)==0):
      sumup+=1
      upspace_all[j]=tmp_upspace[j]
      mid_all.append(j)
    else:
      first_upspace = upspace_all[j]
      second_upspace = tmp_upspace[j]
      final_upspace = {}
      final_upspace['mid']=first_upspace['mid']
      final_upspace['upfollower']=first_upspace['upfollower']
      final_upspace['upname']=first_upspace['upname']
      final_upspace['upface']=first_upspace['upface']
      final_upspace['upsign']=first_upspace['upsign']
      tmp_upvideo = []
      for v in first_upspace['upvideo']:
        if(tmp_upvideo.count(v) == 0):
          tmp_upvideo.append(v)
      for v in second_upspace['upvideo']:
        if(tmp_upvideo.count(v) == 0):
          tmp_upvideo.append(v)
      final_upspace['upvideo']=tmp_upvideo
      final_upspace['video_num']=first_upspace['video_num']+second_upspace['video_num']
total_data['sum_video']=summer
total_data['sum_up']=sumup
print(summer)
print(sumup)
json.dump(aid_all,aidf,ensure_ascii=False)
json.dump(mid_all,midf,ensure_ascii=False)
json.dump(video_all,videof,ensure_ascii=False)
json.dump(upspace_all,upspacef,ensure_ascii=False)
json.dump(total_data,total_dataf,ensure_ascii=False)
for i in range(1, 27):
  f[i - 1].close()
aidf.close()
midf.close()
videof.close()
upspacef.close()