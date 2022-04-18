# -*- coding:utf-8 -*-
from flask import Flask, jsonify,request
import requests
import json
import appbk_sql
import collections
import time
import jieba
from werkzeug.serving import make_server
from wordcloud import WordCloud  
from PIL import Image   
import collections  
from matplotlib import pyplot as plt  
import numpy as np  
import random


app = Flask(__name__,static_folder='static', static_url_path='/static')
app.config['FLASK_ENV'] = 'production'

correct_res = {
    'data': {},
    'status': 200
}


url = "https://c.m.163.com/ug/api/wuhan/app/data/list-total"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4878.0 Safari/537.36"
}


@app.route('/getdata', methods=['GET'])
def refresh():
    use_fake = request.args.get('use_fake')
    data = []
    resault = {}
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sql = "select id,name,value,descrip,url,imageurl,pubdate,scrapy_updatetime from `soaringList`;"
    res = appbk_sql.mysql_com(sql)
    for i in res:
        data.append(
                {'id': i['id'], 'name': i['name'], 'value': i['value'],'descrip':i['descrip'],'url':i['url'],'imageurl':i['imageurl'],'pubdate':i['pubdate']})

    resault['time'] = nowtime
    # 是否使用假数据
    if use_fake == 'true':
        fake_data = [{'id': 1, 'name': '删了吧 (Live)', 'value': 3884, 'descrip': '歌曲名《删了吧 (Live)》，由 郁可唯 演唱，收录于《为歌而赞第二季 第1期》专辑中', 'url': 'http://music.163.com/song?id=1935613660', 'imageurl': 'http://p2.music.126.net/RmpPeKfvUTGmoFNHYv9c3w==/109951167252546807.jpg', 'pubdate': '2022-04-09T00:00:00'}, {'id': 2, 'name': '热铁皮房顶的夏天 (Live)', 'value': 1201, 'descrip': '歌曲名《热铁皮房顶的夏天 (Live)》，由 王赫野 演唱，收录于《为歌而赞第二季 第1期》专辑中', 'url': 'http://music.163.com/song?id=1935607384', 'imageurl': 'http://p2.music.126.net/RmpPeKfvUTGmoFNHYv9c3w==/109951167252546807.jpg', 'pubdate': '1970-01-01T08:00:00'}, {'id': 3, 'name': '呆着', 'value': 1444, 'descrip': '歌曲名《呆着》，由 SeanT肖恩恩、GALI 演唱，收录于《荷尔蒙定律》专辑中', 'url': 'http://music.163.com/song?id=1924568340', 'imageurl': 'http://p2.music.126.net/Cn-y99Dg9xNZF_c2ubagAA==/109951167105426855.jpg', 'pubdate': '1970-01-01T08:00:00'}, {'id': 4, 'name': 'Stray（流浪）', 'value': 2386, 'descrip': '歌曲名《Stray》，别名《流浪》，由 江辰 演唱，收录于《Stray》专辑中', 'url': 'http://music.163.com/song?id=1936399142', 'imageurl': 'http://p1.music.126.net/oV9Do1qmWX6T-xiZBHVALQ==/109951167264308731.jpg', 'pubdate': '2022-04-09T00:00:00'}, {'id': 5, 'name': '苦茶子', 'value': 12570, 'descrip': '歌曲名《苦茶子》，由 Starling8、MoreLearn 27、FIVESTAR 演唱，收录于《苦茶子》专辑中', 'url': 'http://music.163.com/song?id=1922888354', 'imageurl': 'http://p1.music.126.net/x8LI4oQGho-afSQFthr7wg==/109951167084000790.jpg', 'pubdate': '1970-01-01T08:00:00'}, {'id': 6, 'name': '喜劇（TV动画《间谍过家家》片尾曲）', 'value': 2603, 'descrip': '歌曲名《喜劇》，别名《TV动画《间谍过家家》片尾曲》，由 星野源 演唱，收录于《喜劇》专辑中','url': 'http://music.163.com/song?id=1935948260', 'imageurl': 'http://p1.music.126.net/_sGZwt82duHeC0et8lsF0w==/109951167257363569.jpg', 'pubdate': '2022-04-08T00:00:00'}, {'id': 7, 'name': '我是你的谁', 'value': 78, 'descrip': '歌曲名《我是你的谁》，由 RA 演唱，收录于《空白印象》专辑中', 'url': 'http://music.163.com/song?id=1899645471', 'imageurl': 'http://p2.music.126.net/qs57P34e5ybgQayG7CjV_w==/109951166677151057.jpg', 'pubdate': '1970-01-01T08:00:00'}, {'id': 8, 'name': '潮湿', 'value': 46, 'descrip': '歌曲名《潮湿》，由 RA 演唱，收录于《空白印象》专辑中', 'url': 'http://music.163.com/song?id=1899649932', 'imageurl': 'http://p1.music.126.net/qs57P34e5ybgQayG7CjV_w==/109951166677151057.jpg', 'pubdate': '1970-01-01T08:00:00'}, {'id': 9, 'name': 'September Snow（prod by Furyl/4_Chords）', 'value': 3573, 'descrip': '歌曲名《September Snow（prod by Furyl/4_Chords）》，由 谷江山 演唱，收录于《September Snow》专辑中', 'url': 'http://music.163.com/song?id=1936697740', 'imageurl': 'http://p1.music.126.net/zSS8Z9uI5vwdCy1JLpOECQ==/109951167269474740.jpg', 'pubdate': '1970-01-01T08:00:00'}, {'id': 10, 'name': 'Apartment Roof(天台公寓)', 'value': 173, 'descrip': '歌曲名《Apartment Roof(天台公寓)》，由 万万小宇宙 演唱，收录于《FOOD COMA(食物昏迷）》专辑中', 'url': 'http://music.163.com/song?id=1936213732', 'imageurl': 'http://p1.music.126.net/7cv1WCd5el_qnEb67y18tw==/109951167261582862.jpg', 'pubdate': '2022-04-08T00:00:00'}, {'id': 11, 'name': '烛尽', 'value': 45, 'descrip': '歌曲名《烛尽》，由 王杰、Morerare 演唱，收录于《烛尽》专辑中', 'url': 'http://music.163.com/song?id=1930512613', 'imageurl': 'http://p2.music.126.net/yZucknPBClr-4hm6vNWMnA==/109951167181233284.jpg', 'pubdate': '1970-01-01T08:00:00'}, {'id': 12, 'name': 'Foodcoma(食物昏迷)', 'value': 127, 'descrip': '歌曲名《Foodcoma(食物昏迷)》，由 万万小宇宙 演唱，收录于《FOOD COMA(食物昏迷）》专辑中', 'url': 'http://music.163.com/song?id=1936212557', 'imageurl': 'http://p2.music.126.net/7cv1WCd5el_qnEb67y18tw==/109951167261582862.jpg', 'pubdate': '2022-04-08T00:00:00'}, {'id': 13, 'name': '恋爱频率', 'value': 1434, 'descrip': '歌曲名《恋爱频率》，由 Sasablue 演唱，收录于《恋爱频率》专辑中', 'url': 'http://music.163.com/song?id=1928419759', 'imageurl': 'http://p1.music.126.net/RxhofcXQPZNSDZy5GtZAwA==/109951167192765079.jpg', 'pubdate': '1970-01-01T08:00:00'}, {'id': 14, 'name': '空白格 (Live)（原唱：蔡健雅）', 'value': 81229, 'descrip': '歌曲名《空白格 (Live)》，别名《原唱：蔡健雅》，由 杨宗纬 演唱，收录于《我是歌手第一季 第5期》专辑中', 'url': 'http://music.163.com/song?id=25714352', 'imageurl': 'http://p2.music.126.net/s2rrkEZ6S7UVAJI-D1M4lA==/2258396883454110.jpg', 'pubdate': '2013-02-15T00:00:00'}, {'id': 15, 'name': '红色的河 (旅行团 & 吴青峰)', 'value': 694, 'descrip': '歌曲名《红色的河 (旅行团 & 吴青峰)》，由 旅行团、吴青峰 演唱，收录于《似近似远》专辑中', 'url': 'http://music.163.com/song?id=1476233572', 'imageurl': 'http://p1.music.126.net/fh6QJxOBkTlJUj45eA87gg==/109951165291853095.jpg', 'pubdate': '2020-09-16T00:00:00'}]
        for i in fake_data:
            i['value'] = random.randint(5000, 1000000)
        random.shuffle(fake_data)
        resault['data'] = fake_data
    else:
        resault['data'] = data
    return jsonify(resault)




@app.route('/getcovie', methods=['GET'])
def getcovie():
    response = requests.get(url, headers=header)
    data = json.loads(response.text)

    chinese_covid_19_data = []
    for item in data["data"]["areaTree"][2]["children"]:
        tmp = {}
        tmp["name"] = item["name"]
        tmp["today_confirm"] = item["today"]["confirm"]
        tmp["total_confirm"] = item["total"]["confirm"]
        chinese_covid_19_data.append(tmp)
    return jsonify(chinese_covid_19_data)

@app.route('/getwords', methods=['GET'])
def getwords():
    resault = list(np.load("./result.npy",allow_pickle=True))
    return jsonify(resault)

@app.route('/getpythonwords', methods=['POST'])
def getpythonwords():
    text = request.form.get('text')
    background_img = request.form.get('background_img')
    font_style = request.form.get('font_style')
    cut = jieba.cut(text,cut_all=False,HMM=True)
    object_list = []
    stopwords = ['', '就', '月', '，','二是','三是','四是', '为', '》', '人', '均', '《', '：', '将', '右', '系', '们', '并', '。', '新', '也', '）', '学', '对', '一是', '的', '要', '和', '一', '10', '届', '应', '”', '由', '作', ' 间', '“', '以', ' ', '是', '等', '树', '有', '日', '\n', '及', '（', '主', '大', '与', '左', '、', '在', '\\xa0', '项', '型', '；', '年', '给', '下', 
'到', '了', '非', '震', '副', '于','向','各','好','五是']
    stopwords.append('\n')
    #如果单词不在停用词里，则添加
    for word in cut:
        if word not in stopwords:
            object_list.append(word)
    #collections.Counter 计数器，统计单词个数
    word_counts = collections.Counter(object_list)
    img = Image.open('./static/background_img/{}'.format(background_img))
    img_array = np.array(img)  #将图片变为数组
    wc = WordCloud(
        background_color = 'white', # 背景颜色
        mask = img_array,  #遮罩图片
        font_path = './static/font_style/{}'.format(font_style),  #字体样式
        colormap='tab20c'
    )
    wc.generate_from_frequencies(word_counts)  #生成词云图
    fig = plt.figure(1)
    plt.imshow(wc)  # 显示词云
    plt.axis('off') # 关闭保存
    #plt.show()
    #调整边框
    plt.subplots_adjust(top=0.99, bottom=0.01, right=0.99, left=0.01, hspace=0, wspace=0)
    #保存图片
    # plt.savefig(r'./static/'+str(time.time())+'_demo.jpg',dpi = 600)
    # result = {'name':'/api/static/'+str(time.time())+'_demo.jpg'}
    # return result 
    pic_name = './img/'+str(time.time())+'_demo.jpg'
    plt.savefig(pic_name,dpi = 600)
    result = {'name':"/static_api"+pic_name[1:]}
    return result

if __name__ == "__main__":
    server = make_server('127.0.0.1', 8000, app)
    server.serve_forever()
    app.run()
