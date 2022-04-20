# -*- coding:utf-8 -*-
import requests
import json

url = "https://c.m.163.com/ug/api/wuhan/app/data/list-total"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4878.0 Safari/537.36"
}


def mygetcovie():
    response = requests.get(url, headers=header)
    data = json.loads(response.text)

    chinese_covid_19_data = []
    for item in data["data"]["areaTree"][2]["children"]:
        tmp = {}
        tmp["name"] = item["name"]
        tmp["today_confirm"] = item["today"]["confirm"]
        tmp["total_confirm"] = item["total"]["confirm"]
        chinese_covid_19_data.append(tmp)
    return chinese_covid_19_data
