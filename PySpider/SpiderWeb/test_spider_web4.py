import requests
from lxml import etree
url="https://cs.58.com/ershoufang/"
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
page_text=requests.get(url=url,headers=headers).text
tree=etree.HTML(page_text)
#div_list=tree.xpath('//section[@class="list"]/div')
div_list=tree.xpath('//*[@id="esfMain"]/section/section[3]/section[1]/section[2]/div')
fp=open("58.txt","w",encoding="utf-8")
for div in div_list:
    title=div.xpath('./a/div[2]/div[1]/div[1]/h3/@title')
    price=div.xpath('./a/div[2]/div[2]/p[1]/span/text()')
    fp.write("".join(title+price)+"\n")
    print(title+price)
fp.close()
