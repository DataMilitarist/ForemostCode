import requests
from lxml import etree
import re
import pymysql
from time import sleep
from concurrent.futures import ThreadPoolExecutor

def get_conn():
    # 创建连接
    conn = pymysql.connect(host="127.0.0.1",
                           user="root",
                           password="root",
                           db="novels",
                           charset="utf8")
    # 创建游标
    cursor = conn.cursor()
    return conn, cursor

def close_conn(conn, cursor):
    cursor.close()
    conn.close()

def get_xpath_resp(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}
    resp = requests.get(url, headers=headers)
    tree = etree.HTML(resp.text)  # 用etree解析html
    return tree, resp

def get_chapters(url):
    tree, _ = get_xpath_resp(url)
    # 获取小说名字
    novel_name_elements = tree.xpath('//*[@id="info"]/h1/text()')
    if novel_name_elements:
        novel_name = novel_name_elements[0]
    else:
        raise ValueError("novel name not found at the specified XPath")

    # 获取小说数据节点
    dds = tree.xpath('/html/body/div[4]/dl/dd')
    if not dds:
        raise ValueError("No chapter elements found at the specified XPath")

    title_list = []
    link_list = []
    for d in dds[:15]:
        title_elements = d.xpath('./a/text()')
        link_elements = d.xpath('./a/@href')
        if title_elements and link_elements:
            title = title_elements[0]  # 章节标题
            title_list.append(title)
            link = link_elements[0]  # 章节链接
            chapter_url = url + link  # 构造完整链接
            link_list.append(chapter_url)
        else:
            raise ValueError("Title or link not found for a chapter")

    return title_list, link_list, novel_name

def get_content(novel_name, title, url):
    try:
        conn, cursor = get_conn()
        # 插入数据的sql
        sql = 'INSERT INTO novel(novel_name,chapter_name,content) VALUES(%s,%s,%s)'
        tree, resp = get_xpath_resp(url)
        # 获取内容
        content_elements = re.findall('<div id="content">(.*?)</div>', resp.text)
        if content_elements:
            content = content_elements[0]
        else:
            raise ValueError("Content not found for the chapter")
        # 对内容进行清洗
        content = content.replace('<br />', '\n').replace('&nbsp;', ' ').replace(
            '书旗小说<a href="https://t.shuqi.com/reader/8963913/?shuqi_h5=205&chapterId=2130396&forceChapterId=2130396">牧神记</a>最新<br><br>',
            '')
        print(title, content)
        cursor.execute(sql, [novel_name, title, content])  # 插入数据
        conn.commit()  # 提交事务保存数据
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sleep(2)
        close_conn(conn, cursor)  # 关闭数据库

if __name__ == '__main__':
    try:
        # 获取小说名字，标题链接，章节名称
        title_list, link_list, novel_name = get_chapters('https://t.shuqi.com/reader/8963913/?shuqi_h5=205&chapterId=2130396&forceChapterId=2130396')
        with ThreadPoolExecutor(5) as t:  # 创建5个线程
            for title, link in zip(title_list, link_list):
                t.submit(get_content, novel_name, title, link)
                print(title_list)
                print(link_list)
                print(novel_name)
                # 启动线程
    except Exception as e:
        print(f"An error occurred during chapter retrieval: {e}")
