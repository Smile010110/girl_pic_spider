'''
将每张图片的url保存至本地txt文件中
'''
import time
import requests
import urllib.parse
from lxml import etree
from selenium import webdriver
from multiprocessing.dummy import Pool as ThreadPool

text_save_path = "/media/smile/smilewords/cosplay.txt"
url = "https://www.x6o.com/"
cookie = "__cf_bm=I_4h0LwVuF8wz8j7rdAUliMsQgf.MYg.PsqdH1jYKic-1675411382-0-AfvD0yR9vfW8HSckeoXn7ohtF7B1LfYtt3vNqzJQg2yJz3qv0NsBDtPFb5HCfMgt95PixT7NsIq92dWLGFjIu0WFWK36QMge9dF0kXt9Y5/hWGavD9M+UkXbHc96a1iBgyaPrkBEYne/rdy4VbWzGLI="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Cookie": cookie,
}


# 获取写真列表url
def get_articles_url_list(url_):
    novel_url = urllib.parse.urljoin(url_, 'topics/14#articles')
    driver = webdriver.Chrome()  # 启动模拟浏览器
    driver.get(novel_url)  # 打开要爬取的网页地址
    # 获取滚动刷新的网页全部内容
    while True:
        h_before = driver.execute_script('return document.body.scrollHeight;')
        time.sleep(5)
        driver.execute_script(f'window.scrollTo(0,{h_before})')
        time.sleep(5)
        h_after = driver.execute_script('return document.body.scrollHeight;')
        if h_before == h_after:
            break
    content = driver.page_source
    html = etree.HTML(content)
    hrefs = html.xpath('//div[@class="item-list"]/a/@href')
    list_url_ = []
    for href in hrefs:
        chapter_url = urllib.parse.urljoin(url_, href)
        list_url_.append(chapter_url)
    return list_url_


# 下载单个写真集
def save_articles_img(detail_url):
    try:
        print(f"开始获取新的写真---->{detail_url.split('/')[-1]}")
        res = requests.get(detail_url, headers=headers)
        html = etree.HTML(res.text)
        hrefs = html.xpath('//div[@class="mdui-typo content"]//img/@src')
        # 若存在数据 则录入
        if hrefs:
            str_ = '\n'
            f = open(text_save_path, "a")
            f.write(str_.join(hrefs))
            f.close()
            return f"{detail_url}，录入完成，录入数量{len(hrefs)}"
    except requests.exceptions.ConnectTimeout:
        print("下载超时，退出")
    except Exception as ex:
        print(ex)


list_url = get_articles_url_list(url)

# 获取单写真中所有照片的url
pool = ThreadPool()
data = pool.map(save_articles_img, list_url)
pool.close()
pool.join()
