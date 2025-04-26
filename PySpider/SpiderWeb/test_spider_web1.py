import requests
from bs4 import BeautifulSoup
def fetch_website_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"响应失败: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"存在错误: {e}")
        return None
def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup
def main():
    url = 'https://www.hufe.edu.cn/'
    html_content = fetch_website_content(url)
    if html_content:
        soup = parse_html(html_content)
        links = soup.find_all('a')
        for link in links:
            print(link.get('href'))
if __name__ == "__main__":
    main()
