import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
f = open(r'D:\python-crawler\total_data\video_new.json','r',encoding='utf-8')
video = json.load(f)
view = []
coin = []
view_max = 0
coin_max = 0
for v in video:
  if int(v['coin']) < 800 and int(v['view']) < 800:
    view.append(int(v['view']))
    coin.append(int(v['coin']))
    view_max = max(int(v['view']), view_max)
    coin_max = max(int(v['coin']), coin_max)
  if int(v['view']) > 200000:
    print(v['title'])
print('最大播放量：')
print(view_max)
print('最大投币量：')
print(coin_max)
plt.xlabel('view')
plt.ylabel('coin')
plt.scatter(view, coin)
plt.show()
f.close()