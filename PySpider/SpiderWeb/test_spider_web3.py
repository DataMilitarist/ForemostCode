import requests
from lxml import etree
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = 'SimHei'

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}

typ_list=[]
title_list=[]
author_list=[]
num_list=[]
intr_list=[]
D={}
for i in range(1,21):
    url='https://www.hongxiu.com/category/f1_f1_1_f1_f1_f1_0_'+str(i)
    re = requests.get(url, headers=headers)
    re.encoding="gzip"
    tree = etree.HTML(re.text)
    li_list=tree.xpath('/html/body/div[1]/div[2]/div[3]/div[2]/div[1]/ul/li')
    for item in li_list:
        title=item.xpath('./div[2]/h3/a/text()')[0]
        author=item.xpath('./div[2]/h4/a/text()')[0]
        ty=item.xpath('./div[2]/p[1]/span[1]/text()')[0]
        num=item.xpath('./div[2]/p[1]/span[3]/text()')[0][:-1]
        intr=item.xpath('./div[2]/p[2]/text()')[0][2:]
        #print(title)
        title_list.append(title)
        author_list.append(author)
        typ_list.append(ty)
        num_list.append(num)
        intr_list.append(intr)
D={"小说名称":title_list,"作者":author_list,"类型":typ_list,"阅读量(万)":num_list,"小说简介":intr_list}
dt=pd.DataFrame(D)
print(dt)
#1
print(dt.describe())

#2
code=dt["作者"].value_counts()
novel=dt.loc[dt["作者"]=="叶非夜",:]
print(novel)

#3
d=dt.groupby(by='类型').count()
print(d)

#4
dt["阅读量(万)"]=dt["阅读量(万)"].astype(float)
dt=dt.sort_values(by="阅读量(万)",ascending=False)
y=dt["阅读量(万)"].values[0:11]
x=dt["小说名称"].values[0:11]
plt.figure(figsize=(20,10))
plt.bar(x,y)
plt.figure(figsize=(20,10))
labels=dt["类型"].value_counts()
x=list(labels.index)
y=list(labels.values)
plt.pie(y,labels=x,autopct="%0.2f%%")
plt.show()