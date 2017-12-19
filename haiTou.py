# -*- coding: utf-8 -*-
import os
import pymysql
import time
from selenium import webdriver
import bottle
from bottle import route, run



#规则获取
#规则获取
def rule_mysql(sql):
    #数据库查询操作
    try:
        # 获取一个数据库连接，注意如果是UTF-8类型的，需要制定数据库
        conn = pymysql.connect(host='localhost', user='root', passwd='admin', db='test', port=3306, charset='utf8')
        cur = conn.cursor()  # 获取一个游标
        cur.execute(sql)
        result=cur.fetchall()
        rule =result[0]
        cur.close()  # 关闭游标
        conn.close()  # 释放数据库资源
        return rule
    except  Exception:
        print("发生异常")

#海投网
def login():
     sql = 'select * from spider_base_info_v where w_name="海投网" limit 1'
     global  rules
     rules=rule_mysql(sql)
     #先进行登录
     global driver
     #start_urls = ['https://company.haitou.cc/login']
     driver = webdriver.Firefox()
     driver.get(rules[0])
     uname = 'ZHISHENSHUJU'
     password = 'zs123123'
     driver.find_element_by_xpath(rules[4]).send_keys(rules[1])  # 你的用户名
     driver.find_element_by_xpath(rules[5]).send_keys(rules[2])
     driver.find_element_by_xpath(rules[7]).click()
     time.sleep(5)
     driver.get(rules[8])
     time.sleep(3)
     parse(j=1)

def parse(j):
        # #获取爬取规则
        if rules[11] == '是':
            for i in range(1, 31):

                 # try:
                    #      .//*[@id='w1']/table/tbody/tr[num]/td[9]/a
                    title=rules[9]
                    title = title.replace('num',str(i))
                    #print(title)
                    driver.find_element_by_xpath(title).click()
                    time.sleep(2)
                    # 移动句柄为当前页面
                    #driver.switch_to_window(driver.window_handles[1])
                    ##具体爬取数据的方法
                    auto_info(j)
                    j +=1
                    driver.back()
                    #关闭当前句柄
                    #driver.close()
                    #移动句柄
                    #driver.switch_to_window(driver.window_handles[0])
                 # except:
                 #     print("爬取简历完毕！")
        else:
                auto_info(j)

        #翻页
        try:
           driver.find_element_by_xpath(rules[12]).click()
           parse(j)
        except:
           driver.quit()
           print("--------------------------爬取简历结束--------------------------")

def auto_info(j):
     print("简历内容---------------------------------")
     path ="D:/test2/海投网简历库/"
     if  not os.path.exists(path):
         os.makedirs(path)
     path += str(j)
     path +=".txt"
     print(path)
     content = driver.find_element_by_xpath(rules[10]).text
     print(content)
     f = open(path, 'w')
     f.write(content)
     f.write("\n")
     f.close()
@route('/haiTou')#word简历搜索的关键字
def index():
    login()
    return bottle.template('welcome ！！')
run(port=8080, host='localhost')