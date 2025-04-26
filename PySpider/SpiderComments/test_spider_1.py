import csv
import requests
import re
import time
#贴吧评论爬取

def main(page):
    url = f'https://tieba.baidu.com/p/9647682355?pn={page}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }
    resp = requests.get(url, headers=headers)
    html = resp.text
    # 评论内容
    comments = re.findall('style="display:;">                    (.*?)</div>', html)
    # 评论用户
    users = re.findall('class="p_author_name j_user_card" href=".*?" target="_blank">(.*?)</a>', html)
    # 评论时间
    comment_times = re.findall('楼</span><span class="tail-info">(.*?)</span><div', html)
    for u, c, t in zip(users, comments, comment_times):
        # 筛选数据,过滤掉异常数据
        if 'img' in c or 'div' in c or len(u) > 50:
            continue
        csvwriter.writerow((u, t, c))
        print(u, t, c)
    print(f'第{page}页爬取完毕')


if __name__ == '__main__':
    with open('01.csv', 'a', encoding='utf-8') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(('评论用户', '评论时间', '评论内容'))
        for page in range(1, 16):  # 爬取前n页的内容
            main(page)
            time.sleep(2)
