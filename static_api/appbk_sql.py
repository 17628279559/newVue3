#!/usr/bin/env python3
# coding=utf-8
# 功能，appbk数据库访问
# 输入数据库表和sql命令，返回结果
import re
import os
import sys
import time
import json
import datetime
import pymysql
from config import config

pymysql.install_as_MySQLdb()

# 带选择数据库功能

# 数据库
# 带选择数据库功能
g_db_host = config["g_db_host"]  # 服务器
g_db_user = config["g_db_user"]
g_db_pw = config["g_db_pw"]
g_db_name = config["g_db_name"]  # 数据库名
g_db_port = config["g_db_port"]

"""
功能：解决datatime字段输不出json格式错误
"""


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


"""
功能：连接数据
"""


def connect_db(db_name=g_db_name):
    db = ''
    try:
        db = pymysql.connect(host=g_db_host, port=g_db_port, user=g_db_user, passwd=g_db_pw, db=db_name,
                             charset='utf8mb4', connect_timeout=30)
    except Exception as e:
        print("ERROR", e)
        return '-1'

    return db


"""
功能：执行mysql命令，返回结果
输入：sql_com, sql命令
返回：mysql查询结果数组
"""


def mysql_com(sql_com, db_name=g_db_name):
    # 连接数据库
    for i in range(3):
        db = connect_db(db_name)

        if db:
            break
        else:
            i = i + 1

    result = []
    if db != '-1':
        # 执行mysql命令
        # cursor = db.cursor()
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql_com)
        result = cursor.fetchall()
        db.commit()
        db.close()
    return result


"""
功能：执行mysql插入命令
输入：data， 需要插入的数据，list，每行数据为dict，key为数据库字段名，value为数据值
输入：table_name, 数据库名
返回：mysql查询结果数组
"""


def insert_data(data, table_name, db_name=g_db_name):
    # 连接数据库
    for i in range(3):
        db = connect_db(db_name)

        if db:
            break
        else:
            i = i + 1

    if db == '-1':
        return -1

    cursor = db.cursor()

    sqlcom = ""
    key_list = []
    value_list = []
    for item in data:
        key_list.append(item)
        value_list.append("'" + db.escape_string(str(data[item])) + "'")
    key = ",".join(key_list)
    value = ",".join(value_list)

    sqlcom = "insert ignore into  " + table_name + \
        " (" + key + ") values (" + value + ")"
    # sqlcom = "replace into  " + table_name + " (" + key + ") values (" + value + ")"
    try:
        cursor.execute(sqlcom)
        insert_id = int(db.insert_id())  # 插入的自增id
        db.commit()
        db.close()
        return insert_id
    except Exception as e:
        print("ERROR", e)
        return e


"""
功能：执行mysql插入命令,更新插入
输入：data， 需要插入的数据，list，每行数据为dict，key为数据库字段名，value为数据值
输入：table_name, 数据库名
返回：mysql查询结果数组
"""


def insert_update_data(data, table_name, db_name=g_db_name):
    # 连接数据库
    for i in range(3):
        db = connect_db(db_name)

        if db:
            break
        else:
            i = i + 1

    if db == '-1':
        return -1

    cursor = db.cursor()

    key_list = []
    values_insert = ""
    values_update = ""
    for key, values in data.items():
        key_list.append(key)
        values = "'{}'".format(db.escape_string(values)) if type(
            values) == str else "{}".format(values)
        values_insert += values + ','
        values_update_str = "{}={}".format(key, values)
        values_update += values_update_str + ','

    sqlcom = "INSERT into " + table_name + "({}) values ({}) on duplicate key update {}".format(
        ",".join(key_list), values_insert[:-1], values_update[:-1]
    )

    try:
        # print(sqlcom)
        cursor.execute(sqlcom)
        insert_id = int(db.insert_id())  # 插入的自增id
        db.commit()
        db.close()
        return insert_id
    except Exception as e:
        return e


"""
功能: 多行数据插入数据库
输入: data_list, 数据列表
"""


def insert_data_list(data_list, table_name, db_name=g_db_name):
    db = pymysql.connect(host=g_db_host, port=g_db_port, user=g_db_user,
                         passwd=g_db_pw, db=db_name, charset='utf8mb4')
    cursor = db.cursor()

    # step 1, 得到唯一索引列表
    sql = "show create table " + table_name
    cursor.execute(sql)
    result = cursor.fetchall()
    create_str = result[0][1]
    field_list = create_str.split('\n')
    uniq_key_list = []
    for item in field_list:
        if item.find('UNIQUE KEY') != -1:
            m = re.search(r"\(.*\)", item)
            if m:
                uniq_key_str = m.group(0)
                uniq_key_str_new = re.sub('^\(|\)$', '', uniq_key_str)
                uniq_key_list = uniq_key_str_new.split(',')

    # 解析并插入数据
    count_num = 0
    sql_com = ''
    value_args_list = []

    for data in data_list:
        # 每6000条commit一次
        if count_num % 3000 == 0:
            try:
                cursor.executemany(sql_com, value_args_list)
                db.commit()
                # db.close()

                # 重新连接数据库
                # db = MySQLdb.connect(host=db_host, user=db_user, passwd = db_pw, db = db_name, charset='utf8mb4')
                # cursor = db.cursor()

            except Exception as e:
                error_info = 'insert error: ' + str(e)
                print(error_info)
                continue
            value_args_list = []  # 清空数据值list

        key_str = ''
        key_list = []
        value_list = []
        for item in data:
            key_list.append(item)
            if item != '':
                value_list.append(str(data[item]))
            else:
                value_list.append('')

        # part_sql
        part_sql = ""
        for single_key in key_list:
            single_key_1 = "`" + single_key + "`"
            if single_key_1 not in uniq_key_list:
                part_sql = part_sql + single_key + \
                    "=VALUES(" + single_key + "),"
        part_sql_new = re.sub(",$", "", part_sql)

        # sqlcom
        key_str = ",".join(key_list)
        value_num = len(value_list)
        value_sql = ("%s," * value_num).strip(",")
        sql_com = "insert into  " + table_name + \
            " (" + key_str + ") values (" + value_sql + \
            ") on duplicate key update " + part_sql_new

        # value_args
        value_tuple = tuple(value_list)
        value_args_list.append(value_tuple)

    # 执行剩余的数据
    cursor.executemany(sql_com, value_args_list)
    db.commit()
    db.close()
    return 0


if __name__ == "__main__":
    sql_com = 'select * from city limit 10'
    # 默认的db
    result = mysql_com(sql_com)
    for row in result:
        print(row["enName"])
