# -*- coding:utf-8 -*-
import collections
import jieba
from wordcloud import WordCloud
from PIL import Image
import time
import numpy as np

stopwords = ['', '就', '月', '，', '二是', '三是', '四是', '为', '》', '人', '均', '《', '：', '将', '右', '系', '们', '并', '。', '新', '也', '）', '学', '对', '一是', '的', '要', '和', '一', '10', '届', '应', '”', '由', '作', ' 间', '“', '以', ' ', '是', '等', '树', '有', '日', '\n', '及', '（', '主', '大', '与', '左', '、', '在', '\\xa0', '项', '型', '；', '年', '给', '下',
                 '到', '了', '非', '震', '副', '于', '向', '各', '好', '五是', '把', "件", "六是"]
stopwords.append('\n')


def mywordcloud(text, mode, background_color, background_img, font_style):
    cut = jieba.cut(text, cut_all=False, HMM=True)
    object_list = []
    for word in cut:
        if word not in stopwords:
            object_list.append(word)
    word_counts = collections.Counter(object_list)
    img = Image.open('./static/background_img/{}'.format(background_img))
    img_array = np.array(img)  # 将图片变为数组
    wc = WordCloud(
        background_color=background_color,  # 背景颜色
        width=800,
        mode=mode,
        height=800,
        mask=img_array,  # 遮罩图片
        font_path='./static/font_style/{}'.format(font_style),  # 字体样式
        colormap='tab20c'
    )
    print(mode, background_color)
    wc.generate_from_frequencies(word_counts)  # 生成词云图
    pic_name = str(time.time())+'_demo.png'
    wc.to_file('./vue/pythonImg/'+pic_name)
    result = {'name': "/pythonImg/"+pic_name}
    return result


def myjieba(text, num=5):
    cut = jieba.cut(text, cut_all=False, HMM=True)
    object_list = []
    for word in cut:
        if word not in stopwords:
            object_list.append(word)
    word_counts = collections.Counter(object_list)
    result = [{'name': item, 'size': word_counts[item]}
              for item in word_counts if word_counts[item] > num]
    result = sorted(result, key=lambda item: item['size'], reverse=True)
    print(result)
    return result
