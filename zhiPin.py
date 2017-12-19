# -*- coding: utf-8 -*-
import os
import pymysql
import time
from selenium import webdriver
import bottle
from bottle import route, run
import pytesseract
from PIL import Image,ImageEnhance


#规则获取
def rule_mysql(sql):
    #global title
    try:
        # 获取一个数据库连接，注意如果是UTF-8类型的，需要制定数据库
        conn = pymysql.connect(host='localhost', user='root', passwd='admin', db='test', port=3306, charset='utf8')
        cur = conn.cursor()  # 获取一个游标
        cur.execute(sql)
        result=cur.fetchall()
        results =result[0]
        cur.close()  # 关闭游标
        conn.close()  # 释放数据库资源
        return  results
    except  Exception:
        print("发生异常")

#直聘网
def login(keyW):
     sql = 'select * from spider_base_info_v where w_name="boss直聘" limit 1'
     global rules
     rules = rule_mysql(sql)
     print(rules)
     #先进行登录
     global driver
     #start_urls = ['https://www.zhipin.com/user/login.html']
     driver = webdriver.Firefox()
     driver.get(rules[0])
     # uname = '17789650080'
     # password = 'gnfenqi888'
     #code=auto_img()
     driver.find_element_by_xpath(rules[4]).send_keys(rules[1])  # 你的用户名
     driver.find_element_by_xpath(rules[5]).send_keys(rules[2])
     #driver.find_element_by_xpath(".//*[@id='wrap']/div[2]/div[1]/form/div[3]/span[1]/input").send_keys(code)
     time.sleep(5)
     driver.find_element_by_xpath(rules[7]).click()
     time.sleep(5)
     driver.get(rules[8])
     iframe= driver.find_element_by_xpath(rules[14])
     driver.switch_to_frame(iframe)
     driver.find_element_by_xpath(rules[15]).send_keys(keyW)
     time.sleep(2)
     driver.find_element_by_xpath(rules[16]).click()
     #driver.find_element_by_xpath(".//*[@id='container']/div[1]/div[2]/p[2]/button").click()
    # ActionChains(driver).key_down(Keys.ENTER).perform()
     time.sleep(3)
     parse()

def parse():

        global  x
        x=1

        while 1:
         try:

            #title=".//*[@id='search-list']/div[1]/ul/li[num]/a"
            title=rules[9].replace('num',str(x))
            print(title)
            href=driver.find_element_by_xpath(title).get_attribute('href')

            #新窗口打开连接
            newwindow = 'window.open("https://www.baidu.com")'
            driver.execute_script(newwindow)
            driver.switch_to_window(driver.window_handles[1])
            driver.get(href)
            driver.implicitly_wait(5)
            #具体爬取数据的方法
            auto_info(x)
            # 关闭当前句柄
            driver.close()
            # 移动句柄
            driver.switch_to_window(driver.window_handles[0])
            x +=1
         except:
             print("爬取简历完毕！")



def auto_info(j):
     print("简历内容---------------------------------")
     path ="D:/test2/直聘简历库/"
     if  not os.path.exists(path):
         os.makedirs(path)
     path += str(j)
     path +=".txt"
     #driver.refresh()
     content =driver.find_element_by_xpath(rules[10]).text
     print(content)
     f = open(path, 'w')
     f.write(content)
     f.write("\n")
     f.close()
#login()
@route('/zhiPin/<keyW>')#word简历搜索的关键字
def index(keyW):
    login(keyW)
    return bottle.template('welcome ！！')
run(port=8080, host='localhost')