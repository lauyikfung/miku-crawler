from ntpath import realpath
from os import path
import sys
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','mikufans.settings')
import django
django.setup()

import json
from mikudata.models import allup
from mikudata.models import allvideo
upnamef = open(r'D:/python-crawler/mikufans/mikudata/templates/upname.json', 'r', encoding='utf-8')
upsignf = open(r'D:/python-crawler/mikufans/mikudata/templates/upsign.json', 'r', encoding='utf-8')
titlef = open(r'D:/python-crawler/mikufans/mikudata/templates/video_title.json', 'r', encoding='utf-8')
descf = open(r'D:/python-crawler/mikufans/mikudata/templates/video_desc.json', 'r', encoding='utf-8')
upname = json.load(upnamef)
upsign = json.load(upsignf)
title = json.load(titlef)
desc = json.load(descf)
for i in range(0, 5146):
    allvideo.objects.create(vtitle=title[i], vdesc=desc[i])
for i in range(0, 2471):
    allup.objects.create(upname=upname[i], upsign=upsign[i])
upsignf.close()
upnamef.close()
titlef.close()
descf.close()