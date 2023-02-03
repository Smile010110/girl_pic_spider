import os
import requests
import urllib.parse
from lxml import etree
from selenium import webdriver
import time


save_path = "F:/imgs/"
text_save_path = "F:/imgs/cosplay.txt"
url = "https://www.x6o.com/"
cookie = "__cf_bm=I_4h0LwVuF8wz8j7rdAUliMsQgf.MYg.PsqdH1jYKic-1675411382-0-AfvD0yR9vfW8HSckeoXn7ohtF7B1LfYtt3vNqzJQg2yJz3qv0NsBDtPFb5HCfMgt95PixT7NsIq92dWLGFjIu0WFWK36QMge9dF0kXt9Y5/hWGavD9M+UkXbHc96a1iBgyaPrkBEYne/rdy4VbWzGLI="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Cookie": cookie,
}


# 获取写真列表url
def get_articles_url_list(url):
    novel_url = urllib.parse.urljoin(url, 'topics/14#articles')
    driver = webdriver.Chrome()  # 启动模拟浏览器
    driver.get(novel_url)  # 打开要爬取的网页地址
    # 获取滚动刷新的网页全部内容
    while True:
        h_before = driver.execute_script('return document.body.scrollHeight;')
        time.sleep(2)
        driver.execute_script(f'window.scrollTo(0,{h_before})')
        time.sleep(3)
        h_after = driver.execute_script('return document.body.scrollHeight;')
        if h_before == h_after:
            break
    content = driver.page_source
    html = etree.HTML(content)
    hrefs = html.xpath('//div[@class="item-list"]/a/@href')
    list_url = []
    for href in hrefs:
        chapter_url = urllib.parse.urljoin(url, href)
        list_url.append(chapter_url)
    return list_url


# 下载单个写真集中的图片
def save_articles_img(list_url):
    for detail_url in list_url:
        print("开始获取写真---->")
        res = requests.get(detail_url, headers=headers)
        html = etree.HTML(res.text)
        title = html.xpath('//div[@class="mdui-card mdui-card-shadow article"]//h1[@class="title"]/text()')
        if title:
            title = title[0]
        else:
            title = detail_url.split('/')[-1]
        # 创建文件夹
        title_path = save_path + title
        if not os.path.exists(title_path):
            os.mkdir(title_path)
        hrefs = html.xpath('//div[@class="mdui-typo content"]//img/@src')
        if hrefs:
            print(f"开始下载---->{title}")
            with open(text_save_path, "w") as w:
                for href in hrefs:
                    img_name = href.split('/')[-1]
                    res = requests.get(href, headers=headers)
                    if res.status_code == 404:
                        print("图片下载出错---->，准备下载下一张")
                    with open(title_path + '/' + img_name, "wb") as f:
                        f.write(res.content)
                    w.write(f"{href} \n")
            print(f"{title}，下载完成")


list_url = get_articles_url_list(url=url)
save_articles_img(list_url)
