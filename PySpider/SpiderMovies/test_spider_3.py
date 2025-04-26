import re
from time import sleep
import requests
from lxml import etree
import random
import csv


def main(page, f):
    url = f'https://movie.douban.com/top250?start={page * 25}&filter='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.35 Safari/537.36', }
    resp = requests.get(url, headers=headers)
    tree = etree.HTML(resp.text)
    # 获取详情页的链接列表
    href_list = tree.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[1]/a/@href')
    # 获取电影名称列表
    name_list = tree.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[1]/text()')
    for url, name in zip(href_list, name_list):
        f.flush()  # 刷新文件
        try:
            get_info(url, name)  # 获取详情页的信息
        except:
            pass
        sleep(1 + random.random())  # 休息
    print(f'第{i + 1}页爬取完毕')


def get_info(url, name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.35 Safari/537.36',
        'Host': 'movie.douban.com',
    }
    resp = requests.get(url, headers=headers)
    html = resp.text
    tree = etree.HTML(html)
    # 导演
    dir = tree.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')[0]
    # 电影类型
    type_ = re.findall(r'property="v:genre">(.*?)</span>', html)
    type_ = '/'.join(type_)
    # 国家
    country = re.findall(r'地区:</span> (.*?)<br', html)[0]
    # 上映时间
    time = tree.xpath('//*[@id="content"]/h1/span[2]/text()')[0]
    time = time[1:5]
    # 评分
    rate = tree.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')[0]
    # 评论人数
    people = tree.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span/text()')[0]
    print(name, dir, type_, country, time, rate, people)  # 打印结果
    csvwriter.writerow((name, dir, type_, country, time, rate, people))  # 保存到文件中


if __name__ == '__main__':
    # 创建文件用于保存数据
    with open('03-movie-xpath.csv', 'a', encoding='utf-8', newline='') as f:
        csvwriter = csv.writer(f)
        # 写入表头标题
        csvwriter.writerow(('电影名称', '导演', '电影类型', '国家', '上映年份', '评分', '评论人数'))
        for i in range(10):  # 爬取10页
            main(i, f)  # 调用主函数
            sleep(3 + random.random())