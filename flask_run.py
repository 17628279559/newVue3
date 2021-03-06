# -*- coding:utf-8 -*-
from tabnanny import check
from flask import Flask, jsonify, request
from werkzeug.serving import make_server
import numpy as np
import re
from Getwordcloud import mywordcloud, myjieba
from getCovie import mygetcovie
from getCloudMusic import getCloudMusic
from getHtmlContent import myGetHtmlContent
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
    data = mygetcovie()
    return jsonify(data)


@app.route('/getwords', methods=['GET'])
def getwords():
    scrapyUrl = ""
    num = 1
    try:
        scrapyUrl = request.args.get('scrapyUrl')
    except:
        pass
    if not scrapyUrl:
        result = list(np.load("./result.npy", allow_pickle=True))
        return jsonify({'title': 'isnone', 'count': result})
    else:
        data = myGetHtmlContent(scrapyUrl)
        word_counts = myjieba(data['text'])
        result = [{'text': item, 'size': word_counts[item]}
                  for item in word_counts if word_counts[item] > num]
        result = sorted(result, key=lambda item: item['size'], reverse=True)
        return jsonify({'title': data['title'], 'count': result})


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

    if text[:4] == "http":
        text = myGetHtmlContent(text)['text']
    result = mywordcloud(text, mode, background_color,
                         background_img, font_style)
    return result


@app.route('/getDFA', methods=['GET'])
def getDFA():
    normaltype = request.args.get('normaltype').strip()
    allwords = ['(', ')', '|', '*']
    abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
           'h', 'i', 'j', 'k', 'l', 'm', 'n']
    wrongWords = ['()', '(|', '|)', '**', '(*', '||', '|*']
    stack = 0
    wordsnum = False
    if len(normaltype) == 0:
        return {'name': 'extra words', 'wrong': "????????????"}
    for word in normaltype:
        if word not in allwords and word not in abc:
            return {'name': 'extra words', 'wrong': '???????????????'}
        if word == '(':
            stack += 1
        if word == ')':
            stack -= 1
        if word in abc:
            wordsnum = True
    for i in wrongWords:
        if i in normaltype:
            return {'name': 'extra words', 'wrong': '??????????????????'}
    if not wordsnum:
        return {'name': 'extra words', 'wrong': '??????????????????'}
    if stack != 0:
        return {'name': 'extra words', 'wrong': '???????????????'}
    result = normaltype_to_NFA_to_DFA_to_simpleDFA(normaltype)
    return result


if __name__ == "__main__":
    server = make_server('127.0.0.1', 8000, app)
    server.serve_forever()
    app.run()
