# -*- coding: utf-8 -*-
""" 
 @Author   : hawk
 @Email    : a8926764@163.com
 @Time     : 2019/1/31 14:05
 @Version  : 1.0
 @Function : 1.连接数据库；2.创建数据库；3.爬取数据；4.保存到数据库；5.关闭数据库；
"""
import json
import re

import requests
import pymysql
from bs4 import BeautifulSoup as bs

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/70.0.3538.67 Safari/537.36',
}


def parse_first_page(url):
    r = requests.get(url, headers=headers)
    soup = bs(r.text, 'lxml')
    # 查找得到所有的以数字和字母开头的链接
    number_a_list = soup.select('.bus_kt_r1 > a')
    char_a_list = soup.select('.bus_kt_r2 > a')
    # number_a_list = bs(r.text, 'lxml').find('div', class_='bus_kt_r1').find_all('a')
    # char_a_list = bs(r.text, 'lxml').find('div', class_='bus_kt_r2').find_all('a')
    # 提取a里面的href
    a_list = number_a_list + char_a_list
    href_list = []
    for oa in a_list:
        href = url.rstrip('/') + oa['href']
        href_list.append(href)
    return href_list


def parse_second_page(url, href):
    r = requests.get(url=href, headers=headers)
    soup = bs(r.text, 'lxml')
    # 查找得到所有的公交链接
    bus_a_list = soup.select('#con_site_1 > a')
    href_list = []
    for oa in bus_a_list:
        href = url.rstrip('/') + oa['href']
        href_list.append(href)
    return href_list


def parse_third_page(href, fp):
    r = requests.get(href, headers=headers)
    soup = bs(r.text, 'lxml')
    try:
        # 线路名称
        route_name = soup.select('.bus_i_t1 > h1')[0].string.lstrip("郑州").split("公交车路线&nbsp")[0]
        print('正在爬取---%s---...' % route_name)

        # 运行时间
        run_time = soup.select('.bus_i_content > p')[0].string.lstrip("运行时间：")
        str1 = "|"
        up_time = run_time[:run_time.index(str1)]
        dw_time = run_time[run_time.index(str1):][1:]

        # 票价信息
        price = soup.select('.bus_i_content > p')[1].string.split("票价信息：票价")[-1].split(",")[0]

        # 公交公司
        company = soup.select('.bus_i_content > p > a')[0].string
        # 更新时间
        update_time = soup.select('.bus_i_content > p')[-1].string.lstrip('最后更新：')
        # 上行总个数
        up_total = soup.select('.bus_line_top > span')[0].string.strip('共站').strip()
        # 上行总站牌
        up_name_list = []
        number = int(up_total)
        up_a_list = soup.select('.bus_site_layer > div > a')[:number]
        for oa in up_a_list:
            up_name_list.append(oa.string)
        # 下行总个数
        # 下行总站牌
        down_a_list = soup.select('.bus_site_layer > div > a')[number:]
        down_name_list = []
        down_total = len(down_a_list)
        for oa in down_a_list:
            down_name_list.append(oa.string)

        # 保存到字典中
        item = {
            'bname': route_name,
            'uptime': up_time,
            'dwtime': dw_time,
            'price': price,
            'company': company,
            'updata': update_time,
            'upcount': up_total,
            'upsite': up_name_list,
            'dwcount': down_total,
            'dwsite': down_name_list,
        }
        string = json.dumps(item, ensure_ascii=False)
        fp.write(string + '\n' + ',')
        print('结束爬取---%s---' % route_name)
        # return string
    except Exception:
        pass


# time.sleep(1)


# 爬取数据，保存到txt文件中。
def fp(url, fn):
    all_list = parse_first_page(url)
    fp = open(fn, 'w', encoding='utf8')
    # 解析二级页面
    for href in all_list:
        bus_href_list = parse_second_page(url, href)
        # 遍历所有的公交详情页，获取每一路公交的详细信息
        for href_detail in bus_href_list:
            parse_third_page(href_detail, fp)
    fp.close()


# 初始化，创建数据表businfo
def init():
    try:
        cur.execute("DROP TABLE IF EXISTS businfo")  # 创建数据表businfo
        # 创建表SQL语句
        sql = "CREATE TABLE businfo (id int primary key auto_increment,bname varchar(50) not null,uptime varchar(50),dwtime varchar(50),price varchar(50) ,company varchar(50),updata varchar(32),upcount varchar(32),upsite varchar(500),dwcount varchar(32),dwsite varchar(500));"
        cur.execute(sql)  # 执行创建数据操作
        print("------------Create Database Succeed--------------")
    except:
        cur.execute("USE smartbus")  # 切换到该数据库


# 保存到数据库。
def store(a, b, c, d, e, f, g, h, i, j):  # 少两个字段 upste和dwsite
    # 插入数据到数据库sql语句，%s用作字符串占位
    sql = "INSERT INTO businfo(bname,uptime,dwtime,price,company,updata,upcount,dwcount,upsite,dwsite) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cur.execute(sql, (a, b, c, d, e, f, g, h, i, j))
    cur.connection.commit()


# 截取字符串从第一个数字开始的以后字符
def spl(str):
    char1 = re.search('\d+', str).group()
    char2 = char1[0]
    pos = str.index(char2)
    return str[pos:]


# 读取数据
def readtxt(fn):
    # 逐条读数据，逐条写入mysql.businfo表
    for line in open(fn, 'r', encoding='utf-8'):    # 逐条读取数据
        a = line.strip(',')                         # 去除数据末尾的，
        M = json.loads(a)                           # 将字符串转为字典
        M['uptime'] = spl(M['uptime'])              # 从数字开始截取
        M['dwtime'] = spl(M['dwtime'])              # 从数字开始截取
        M['upsite'] = ','.join(M['upsite'])         # list转为字符串
        M['dwsite'] = ','.join(M['dwsite'])         # list转为字符串
        store(M['bname'], M['uptime'], M['dwtime'], M['price'], M['company'], M['updata'], M['upcount'], M['dwcount'],
              M['upsite'], M['dwsite'])


def main():
    city = 'zhengzhou'                              # 创建城市，用拼音
    url = 'http://' + city + '.8684.cn'             # 选择网址，选择目标url网址
    fn = '' + city + '.txt'                         # 配置文件，配置存放数据的文件路径和文件名
    # fp(url, fn)                                   # 爬取数据，并保存到配置的txt文件中
    # init()                                        # 初始化中，创建数据库表 businfo
    # readtxt(fn)                                   # 读取数据，并保存到数据库


if __name__ == '__main__':
    try:
        # 连接数据库，获取游标
        db = pymysql.connect(host="localhost", user="root", password="Mice_6226", db="mysql", charset="utf8")
        # 创建一个游标对象
        cur = db.cursor()
        print("----------SQL Connection Succeed!-------------")

    except:
        print("-------Warning! SQL Connection Failed!--------")

    main()

    try:
        cur.close()
        db.close()
        print("-----------SQL Connection Closed--------------")
        print("-------------------Over-----------------------")
    except:
        print("------Warning! Can't close Connection!--------")
