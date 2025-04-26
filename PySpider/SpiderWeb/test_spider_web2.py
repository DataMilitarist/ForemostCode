import requests
from lxml import etree
url="https://www.shicimingju.com/book/hongloumeng.html"
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
re=requests.get(url,headers=headers)
re.encoding="utf=8"
data=re.text
tree=etree.HTML(data)
a_list=tree.xpath('/html/body/div[2]/div[2]/div[1]/div[3]/div/a')
fp=open("sanguotest.txt","w",encoding="utf-8")
for item in a_list:
    title=item.text
    url="https://www.shicimingju.com"+item.xpath('.//@href')[0]
    re_page=requests.get(url,headers=headers)
    re_page.encoding="utf-8"
    data_page=re_page.text
    tree=etree.HTML(data_page)
    content=tree.xpath('/html/body/div[2]/div[2]/div[1]/div[2]/div/p/text()')
    fp.write(title+"\n")
    fp.writelines(content)
    fp.write('*************************************************************'+"\n")
    print(title)
