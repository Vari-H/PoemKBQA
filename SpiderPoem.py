import csv
import os
import time

import requests
from lxml import etree


class Spider:
    def __init__(self, url):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/99.0.4844.82 Safari/537.36 '
        }
        self.base_url = 'https://so.gushiwen.cn'
        self.start_url = url

    def crawl_title(self, csv_name, tag):
        html = requests.get(self.start_url, headers=self.headers).content
        # print(html)
        selector = etree.HTML(html)
        poem_link = selector.xpath("//div[@class='typecont']//@href ")
        file_path = os.path.split(os.path.realpath(__file__))[
                        0] + os.sep + "poemData" + os.sep + "csv" + os.sep + csv_name + ".csv"

        csvfile = open(file_path, "a+", encoding='utf-8', newline='')
        for link in poem_link:
            url = self.base_url + link
            # print(url)
            res = requests.get(url, headers=self.headers).content
            selector = etree.HTML(res)
            title = selector.xpath("//div[@class='cont']//h1/text()")[0]
            print(title)

            # 朝代
            dynasty_str = selector.xpath("//div[@class='cont']//p[@class='source']/a/text()")
            dynasty = dynasty_str[1].lstrip("〔").rstrip("〕")
            # 作者
            author = dynasty_str[0]

            # print(dynasty)
            # print(author)

            # 内容
            c = selector.xpath("//div[@class='sons'][1]//div[@class='contson']")[0]
            info = c.xpath("string(.)")

            content = ''
            content = content.join(info).replace('\n', '').replace('\r', '').replace(' ', '').strip()  # 去掉所有的回车和换行和空格
            # print(content)

            writer = csv.writer(csvfile)
            data_row = [author, dynasty, title, content, tag]
            writer.writerow(data_row)
        csvfile.close()

    def start(self, csv_name, tag):
        self.crawl_title(csv_name, tag)


def merge(file_path):
    with open("poemData/csv/all.csv", "a+", encoding='utf-8', newline='') as f:
        file = open(file_path, "r", encoding='utf-8')
        reader = csv.reader(file)
        writer = csv.writer(f)
        for item in reader:
            writer.writerow(item)


if __name__ == '__main__':
    url_list = [
        'https://so.gushiwen.cn/gushi/chuntian.aspx',
        'https://so.gushiwen.cn/gushi/xiatian.aspx',
        'https://so.gushiwen.cn/gushi/qiutian.aspx',
        'https://so.gushiwen.cn/gushi/dongtian.aspx',
        'https://so.gushiwen.cn/gushi/feng.aspx',
        'https://so.gushiwen.cn/gushi/hua.aspx',
        'https://so.gushiwen.cn/gushi/xue.aspx',
        'https://so.gushiwen.cn/gushi/yueliang.aspx',
        'https://so.gushiwen.cn/gushi/shanshui.aspx',
        'https://so.gushiwen.cn/gushi/jieri.aspx'
    ]
    name_list = ['chuntian', 'xiatian', 'qiutian', 'dongtian', 'feng', 'hua', 'xue', 'yueliang', 'shanshui', 'jieri']
    tag_list = ['春', '夏', '秋', '冬', '风', '花', '雪', '月', '山水', '节日']
    for i in range(0, 10):
        print("开始爬取", url_list[i], name_list[i], tag_list[i])
        pp = Spider(url_list[i])
        pp.start(name_list[i], tag_list[i])
        time.sleep(6)
        print("等待6秒......")
