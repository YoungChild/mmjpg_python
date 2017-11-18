#!/usr/bin/evn python
# -*- coding:utf-8 -*-
# __author__:
import urllib2
import bs4
import time
import requests
import fake_useragent
import os
import re
import sys
import xlrd
import random

# 用于将u 转换成 string
reload(sys)
sys.setdefaultencoding('utf-8')  # u -> str


class GetPictures(object):
    def __init__(self):
        self.url = 'http://www.mmjpg.com/mm/1'
        self.first_num = 0
        self.sum_num = 0
        self.pictures_sum()
        self.urls = self.get_urls()
        for url in self.urls:
            self.down_pictures(self.get_img_urls(url))

    # 输入需要的套数
    def pictures_sum(self):
        str1 = raw_input(r"第几套开始，重复会跳过")
        try:
            self.first_num = int(float(str1))
        except ValueError:
            print ('输入的不为数字')

        str1 = raw_input("收集多少套")
        try:
            self.sum_num = int(float(str1))
        except ValueError:
            print("输入的不为数字")
            exit(1)

    # 得到所有套图的第一张所在网页的URL
    def get_urls(self):
        urls = []
        for i in xrange(self.first_num, self.first_num+self.sum_num):
            url_split = self.url.split('/')
            url_split[-1] = str(i)
            urls.append('/'.join(url_split))
        # print urls
        return urls

    # 得到一共有多少张图
    def get_img_sum_num(self, img_url):
        fa = fake_useragent.UserAgent()
        headers = {'User-Agent': fa.random,
                   'Referer': 'http://www.mmjpg.com'}
        request = requests.get(img_url, headers=headers)
        soup = bs4.BeautifulSoup(request.content, 'lxml')
        # 获取标签里面的值
        img_sum_number = soup.find_all('a', href=re.compile('/mm'))[8].get_text().strip()
        print img_sum_number
        img_sum_number = int(img_sum_number)
        # print img_sum_number
        return img_sum_number

    # 得到该套图中的所有图片的URL
    def get_img_urls(self, url):
        fa = fake_useragent.UserAgent()
        headers = {'User-Agent': fa.random,
                   'Referer': 'http://m.mmjpg.com'}
        request = requests.get(url, headers=headers)
        soup = bs4.BeautifulSoup(request.content, 'lxml')
        first_img_url = soup.find('img').get('src')     # 获取标签值
        url_split = first_img_url.split('/')
        img_urls = []
        for i in xrange(1, self.get_img_sum_num(url)+1):
            url_split[-1] = (str(i)+'.jpg')
            img_urls.append('/'.join(url_split))
        # print img_urls
        return img_urls

    # 下载图片
    def down_pictures(self, img_urls):
        img_name = str(img_urls[0].split('/')[-2])+'-'+str(img_urls[0].split('/')[-3])
        if os.path.exists(img_name):    # 查重 如果这个文件夹存在则跳过 防止重复下载
            time.sleep(1)
            print img_name+'存在'
            return
        os.mkdir(img_name)
        for img_url in img_urls:
            fa = fake_useragent.UserAgent()
            headers = {'User-Agent': fa.random,
                       'Referer': 'http://m.mmjpg.com'}
            request = requests.get(img_url, headers=headers)

            with open(img_name + u'/' + img_url.split('/')[-1], 'wb') as f:
                f.write(request.content)    # contents返回的为二进制   text返回的为union类型
                f.close()
                print "已保存" + img_name + '/' + img_url.split('/')[-1]
                time.sleep(random.random()*2)


# 运行程序
if __name__ == '__main__':
    GetPictures()

'''
用requests,bs4 抓取mmjpg.com上的套图
将上面的套图按套进行保存
'''