# -*- coding:utf-8 -*-
import requests
import json
from config import config

BASE_URL = config["spider_api"]
header = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,rw;q=0.8",
    "Connection": "keep-alive",
    "Aontent-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "spider.kappbk.com",
    "Origin":"http://spider.kappbk.com",
    "Referer": "http://spider.kappbk.com/news_parser/html/test_demo.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}


parmas = {"token":config["spider_token"],"url":""}

def myGetHtmlContent(url):
    if not url:
        return "None"
    parmas['url'] = url
    response = requests.post(BASE_URL, data=json.dumps(parmas),headers=header)
    data = json.loads(response.text)
    return {'title':data['title'],'text':data['contents'].replace('\n','')}