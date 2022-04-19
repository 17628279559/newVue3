# -*- coding:utf-8 -*-
from tabnanny import check
from flask import Flask, jsonify, request
from werkzeug.serving import make_server
import numpy as np
import re
from Getwordcloud import mywordcloud, myjieba
from getCovie import getcovie
from getCloudMusic import getCloudMusic
from getSimpleDFA import normaltype_to_NFA_to_DFA_to_simpleDFA


app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['FLASK_ENV'] = 'production'


@app.route('/getdata', methods=['GET'])
def getcloud():
    use_fake = request.args.get('use_fake')
    result = getCloudMusic(use_fake)
    return jsonify(result)


@app.route('/getcovie', methods=['GET'])
def getcovie():
    data = getcovie()
    return jsonify(data)


@app.route('/getwords', methods=['GET'])
def getwords():
    result = list(np.load("./result.npy", allow_pickle=True))
    return jsonify(result)


@app.route('/getjiebacut', methods=['GET'])
def getjiebacut():
    text = request.args.get('text')
    try:
        num = request.args.get('num')
    except:
        num = 5
    result = myjieba(text, num)
    return jsonify(result)


@app.route('/getpythonwords', methods=['POST'])
def getpythonwords():
    text = request.form.get('text')
    background_img = request.form.get('background_img')
    font_style = request.form.get('font_style')
    is_transparent = request.form.get('is_transparent')
    mode = "RGB"
    background_color = 'white'
    if is_transparent == "True":
        mode = "RGBA"
        background_color = "rgba(0,0,0,0)"

    result = mywordcloud(text, mode, background_color,
                         background_img, font_style)
    return result


@app.route('/getDFA', methods=['GET'])
def getDFA():
    normaltype = request.args.get('normaltype').strip()
    allwords = ['(', ')', '|', '*']
    abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
           'h', 'i', 'j', 'k', 'l', 'm', 'n']
    stack = 0
    wordsnum = False
    if len(normaltype) == 0:
        return {'name': 'extra words', 'wrong': "输入为空"}
    for word in normaltype:
        if word not in allwords and word not in abc:
            return {'name': 'extra words', 'wrong': '有非法字符'}
        if word == '(':
            stack += 1
        if word == ')':
            stack -= 1
        if word in abc:
            wordsnum = True
    if re.search('\(\)', normaltype) or re.search('\*\*', normaltype) or not wordsnum:
        return {'name': 'extra words', 'wrong': '无意义表达式'}
    if stack != 0:
        return {'name': 'extra words', 'wrong': '括号不匹配'}
    result = normaltype_to_NFA_to_DFA_to_simpleDFA(normaltype)
    return result


if __name__ == "__main__":
    server = make_server('127.0.0.1', 8000, app)
    server.serve_forever()
    app.run()
