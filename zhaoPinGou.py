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

    try:
        # 获取一个数据库连接，注意如果是UTF-8类型的，需要制定数据库
        conn = pymysql.connect(host='localhost', user='root', passwd='admin', db='test', port=3306, charset='utf8')
        cur = conn.cursor()  # 获取一个游标
        cur.execute(sql)
        result=cur.fetchall()
        content =result[0]
        cur.close()  # 关闭游标
        conn.close()  # 释放数据库资源
        return content
    except  Exception:
        print("发生异常")
#招聘狗
def login():
     sql = 'select * from spider_base_info_v where w_name="招聘狗" limit 1'
     global rules
     rules = rule_mysql(sql)
     print(rules)
     #先进行登录
     global driver
     # start_urls = ['http://qiye.zhaopingou.com/']
     driver = webdriver.Firefox()
     driver.get(rules[0])


     # uname = '17789126120'
     # password = 'zs123123'
     driver.find_element_by_xpath(rules[4]).send_keys(rules[1])  # 你的用户名
     driver.find_element_by_xpath(rules[5]).send_keys(rules[2])
    # time.sleep(3)
     try:
       driver.find_element_by_xpath(rules[17]).click()
     except:
         print("不需要选择地点")
     #driver.find_element_by_xpath(".//*[@id='captcha']").send_keys(code)

    #
     driver.find_element_by_xpath(rules[7]).click()
     time.sleep(6)
     #
     read = open("D:/test2/招聘狗简历库/zhaoPinGou.txt", 'r',encoding='utf-8')  # 返回一个文件对象
     lines = read.readlines()  # 调用文件的 readline()方法
     for line in lines:

         if line.find(address) != -1:
             address_no = line.replace(address, '').strip()
             print(address_no)
             break
     read.close()
     #http://qiye.zhaopingou.com/resume?hopeAdressStr=1&key=java
     #http://qiye.zhaopingou.com/resume?hopeAdressStr=adress_no&key=keyWord
     link =rules[8].replace('adress_no',address_no)
     link =link.replace('keyWord',keyWord)

     driver.get(link)
     time.sleep(10)
     #driver.implicitly_wait(10)

     #
     parse()

def parse():
        # #获取爬取规则
        # sql = "SELECT t.title,t.content FROM zhi_lian_RULE t"
        # rule_mysql(sql)
        #j = 1
        for i in range(1, 26):
            if rules[11] == "是":
              try:
                 #.//*[@id='js_resSearch']/div[3]/div[2]/h3/a
                #.//*[@id='wrapDiv']/div/div[1]/div[4]/div[3]/dl/div/dd[num]/a/div/ul/li[1]/p
                title=rules[9].replace('num',str(i))
                driver.find_element_by_xpath(title).click()
               #driver.implicitly_wait(7)
                time.sleep(4)
                # 移动句柄为当前页面
                all=driver.window_handles
                z=driver.current_window_handle

                driver.switch_to_window(driver.window_handles[1])
                ##具体爬取数据的方法
                auto_info()

                #print(content)
                #关闭当前句柄
                driver.close()
                #移动句柄
                driver.switch_to_window(driver.window_handles[0])
              except:
                 print("爬取简历完毕！")
                 break
            else:
                auto_info()

        #翻页
        try:
           driver.find_element_by_xpath(rules[12]).click()
           time.sleep(3)
           parse()
        except:
           driver.quit()
           print("--------------------------爬取简历结束--------------------------")

def auto_info():
  # try:
     print("简历内容---------------------------------")
     content = driver.find_element_by_xpath(rules[10]).text
     print(content)
     path ="D:/test2/招聘狗简历库/"+address+"/"+keyWord+"/"
     txt_name = str(driver.find_element_by_xpath(".//*[@id='resume_information_center']/div[1]/div/div[1]/div/span[1]").text)

     name,no=txt_name.split("：")
     no = no.strip()
     if  not os.path.exists(path):
         os.makedirs(path)
     path += no
     path +=".txt"
     print(path)
     f = open(path, 'w')

     f.write(content)
     f.write("\n")
     f.close()
   # except:
   #     print("该简历爬取失败")
   #   #print(work_position)
# address='1'
# keyWord='java'
# login()

@route('/zhaoPinGou/<addr>/<keyW>')#word简历搜索的关键字
def index(addr,keyW):
    global address
    global keyWord
    address=str(addr)
    keyWord=str(keyW)
    login()
    return bottle.template('welcome {{name}}！！', name=keyWord)
run(port=8080, host='localhost')