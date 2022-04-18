#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#coding = utf-8
from datetime import datetime
from Crypto.Cipher import AES
from base64 import b64encode
import requests
import re
import time
import os
import json
import random
import appbk_sql
from lxml import etree
from copy import deepcopy

BASE_URL = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token="
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4878.0 Safari/537.36"
}


i4m = {
    "csrf_token": "",
    "cursor": "-1",
    "offset": "0",  # 偏移量，前面每页评论数的总和pageSize
    "orderType": "1",
    "pageNo": "1",  # 页数
    "pageSize": "20",  # 页评论数
    "rid": "R_SO_4_{}",
    "threadId": "R_SO_4_{}"
}


bsR5W2 = "010001"
bsR5W3 = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
bsR5W4 = "0CoJUm6Qyw8W8jud"

random_num = "d5bpgMn9byrHNtAh"  # 随机值，取啥无所谓，这里直接固定了
iv = "0102030405060708"  #函数内部调用的一个固定值

def get_encSecKey():    # 因为random_num固定了，这里返回固定值
    return "1b5c4ad466aabcfb713940efed0c99a1030bce2456462c73d8383c60e751b069c24f82e60386186d4413e9d7f7a9c7cf89fb06e40e52f28b84b8786b476738a12b81ac60a3ff70e00b085c886a6600c012b61dbf418af84eb0be5b735988addafbd7221903c44d027b2696f1cd50c49917e515398bcc6080233c71142d226ebb"

def get_params(data):  
    first = enc_params(data, bsR5W4)
    second = enc_params(first, random_num)
    return second  

def to_16(data):  # 转化成16的倍数, 位下方的加密算法服务
    pad = 16 - len(data) % 16
    data += chr(pad) * pad
    return data

def enc_params(data, key):  # 加密过程
    data = to_16(data)
    aes = AES.new(key=key.encode("utf-8"), IV=iv.encode('utf-8'),
                  mode=AES.MODE_CBC)  # 创建加密器
    bs = aes.encrypt(data.encode("utf-8"))  # 加密, 加密的内容的长度必须是16的倍数
    return str(b64encode(bs), "utf-8")  # 转化成字符串返回,


def get_song_id():
    listurl = 'https://music.163.com/discover/toplist'
    while True:
        response = requests.get(listurl, headers=header)
        html = etree.HTML(response.text)
        url = html.xpath('//ul[@class="f-hide"]/li/a/@href')[:15]
        for i in range(15):
            try:
                run(re.search("id=([\d]+)", url[i]
                              ).group(1), i+1)
                time.sleep(random.random()/2)
            except Exception as e:
                print("Error:", e)
        time.sleep(1800)


def run(song_id, id):
    surl="https://music.163.com/song?id={}"
    new_i4m = deepcopy(i4m)
    new_i4m["rid"] = new_i4m["rid"].format(song_id)
    new_i4m["threadId"] = new_i4m["threadId"].format(song_id)

    resp = requests.post(BASE_URL, data={
        "params": get_params(json.dumps(new_i4m)),
        "encSecKey": get_encSecKey()
    })
    resp2 = requests.get(surl.format(song_id),headers=header)
    info = re.search('<script type="application/ld\+json">([^<]+)</script>',resp2.text).group(1)
    info = eval(info)
    
    comment_num = resp.json()["data"]["totalCount"]
    url=info['@id']
    song_name = info['title'].replace('"','\"').replace("'","\'")
    try:
        images = info['images'][0]
    except:
        print('可能没有图片')
    desc = info['description'].replace('"','\"').replace("'","\'")
    pubdate = info['pubDate']
    scrapy_updatetime = str(datetime.now())


    sql = "UPDATE `soaringList` SET `name`='{}',`value`={},`descrip`='{}',`url`='{}',`imageurl`='{}',`pubdate`='{}',`scrapy_updatetime`='{}' WHERE `id` = {};"
    sql = sql.format(song_name, str(comment_num),desc,url,images,pubdate,scrapy_updatetime,str(id))
    print(sql)
    appbk_sql.mysql_com(sql)


if __name__ == "__main__":
    # run("1929025019",1)
    get_song_id()
