import random
import urllib.request
from bs4 import BeautifulSoup
import codecs
from time import sleep


def main(url, headers):
    page = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(page)
    contents = page.read()

    soup = BeautifulSoup(contents, "html.parser")

    # 打印表头
    print(f"序号\t电影名称\t链接\t主演\t上映时间\t评分\t")

    for tag in soup.find_all(attrs={"class": "item"}):
        num = tag.find('em').get_text()
        print(num, end='\t')

        name = tag.find_all(attrs={"class": "title"})
        zwname = name[0].get_text()
        print(zwname, end='\t')

        url_movie = tag.find(attrs={"class": "hd"}).a
        urls = url_movie.attrs['href']
        print(urls, end='\t')

        info = tag.find(attrs={"class": "star"}).get_text()
        info = info.replace('\n', ' ').replace('/', '').split()[0]
        print(info, end='\t')

        date = tag.find(attrs={"class": "date"})
        if date:
            print(date.get_text(), end='\t')
        else:
            print('-', end='\t')

        cast_info = tag.find(attrs={"class": "bd"})
        if cast_info:
            cast_list = cast_info.find_all('a')
            if cast_list:
                cast_names = [cast.get_text() for cast in cast_list]
                print(len(cast_names), end='\t')
            else:
                print('-', end='\t')
        else:
            print('-', end='\t')

        print('-')  # 主演和投票人数暂时无法从现有结构中获取


sleep(5 + random.random())

if __name__ == '__main__':
    infofile = codecs.open("03-movie-bs4.txt", 'a', 'utf-8')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

    i = 0
    while i < 10:
        print('页码', (i + 1))
        num = i * 25
        url = f'https://movie.douban.com/top250?start={num}&filter='
        main(url, headers)
        infofile.write("\r\n\r\n")
        i += 1
    infofile.close()
