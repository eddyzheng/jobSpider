# -*- coding: utf-8 -*-
import os
import pymysql
import time
from selenium import webdriver
import bottle
from bottle import route, run


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



#百财网
def login():
     #先进行登录
     sql = 'select * from spider_base_info_v where w_name="百才招聘网" limit 1'
     global  rules
     rules=rule_mysql(sql)
     global driver
     #
     driver = webdriver.Firefox()
     driver.get(rules[0])

     driver.find_element_by_xpath(rules[3]).click()
     driver.implicitly_wait(2)

     driver.find_element_by_xpath(rules[4]).send_keys(rules[1])  # 你的用户名
     driver.find_element_by_xpath(rules[5]).send_keys(rules[2])
     driver.find_elements_by_xpath(rules[7])[1].click()
     time.sleep(5)
     link =rules[8]
     link=link.replace('keyword',keyWord)
     link = link.replace('address',address)
     driver.get(link)
     print(rules[11])
     time.sleep(3)

     # 当前信息有多少
     parse()

def parse():
        #获取爬取规则
        for i in range(1, 21):
         if rules[11] =="是" :
             print('----------------------22222222222222222222--------------')
             try:#".//*[@id='resumesList']/li[num]/a"
                title=rules[9]
                #获取当前句柄
                driver.current_window_handle
                #获取所有窗口的句柄
                driver.window_handles

                title=title.replace("num",str(i))
                driver.find_element_by_xpath(title).click()
                time.sleep(2)
                # 移动句柄为当前页面
                driver.switch_to_window(driver.window_handles[1])
                ##具体爬取数据的方法
                auto_info()

                #关闭当前句柄
                driver.close()
                #移动句柄
                driver.switch_to_window(driver.window_handles[0])
             except:
                 print("爬取简历完毕！")
         else:
             auto_info()

        #翻页
        try:
           driver.find_element_by_xpath(rules[12]).click()
           parse()
        except:
           driver.quit()
           print("--------------------------爬取简历结束--------------------------")

def auto_info():
     print("简历内容---------------------------------")
     path ="D:/test2/百才网简历库/"+address+"/"+keyWord+"/"
     txt_name = driver.find_element_by_xpath("html/body/div[2]/div/div[1]/table[2]/tbody/tr/td[4]/p/span").text
     if  not os.path.exists(path):
         os.makedirs(path)
     path += txt_name
     path +=".txt"
     print(path)
     content = driver.find_element_by_xpath(rules[10]).text
     f = open(path, 'w')
     f.write(content)
     f.write("\n")
     f.close()
     #print(work_position)
# address='西安'
# keyWord='文员'
@route('/baiCai/<addr>/<keyW>')#word简历搜索的关键字
def index(addr,keyW):
    global address
    global keyWord
    address=str(addr)
    keyWord=str(keyW)
    login()
    return bottle.template('welcome {{name}}！！', name=keyWord)
run(host='localhost', port=8080)
