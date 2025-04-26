import requests
import csv
from time import sleep
import random


def main(page, f):
    url = ''
    params = {
        'productId': 100011483893,
        'score': 0,
        'sortType': 5,
        'page': page,
        'pageSize': 10,
        'isShadowSku': 0,
        'fold': 1
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.35 Safari/537.36',
        'referer': 'https://item.jd.com/'
    }
    resp = requests.get(url, params=params, headers=headers).json()
    comments = resp['comments']
    for comment in comments:
        content = comment['content']
        content = content.replace('\n', '')
        comment_time = comment['creationTime']
        score = comment['score']
        print(score, comment_time, content)
        csvwriter.writerow((score, comment_time, content))
    print(f'第{page + 1}页爬取完毕')


if __name__ == '__main__':
    with open('04.csv', 'a', encoding='utf-8', newline='') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(('评分', '评论时间', '评论内容'))
        for page in range(15):
            main(page, f)
            sleep(5 + random.random())