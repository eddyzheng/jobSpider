# -*- coding: utf-8 -*-
import os
import pymysql
import time
import bottle
from bottle import route, run
import os
from selenium import webdriver
chromepath=os.path.abspath(r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
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

#智联招聘信息，爬取
def login():
    #爬虫规则
     sql = 'select * from spider_base_info_v where w_name="智联招聘网" limit 1'
     global  rules
     rules=rule_mysql(sql)
     print(rules)
     #先进行登录
     global driver
     #start_urls = ['https://passport.zhaopin.com/org/login?DYWE=1500951340319.109686.1500951340.1500951340.1&y7bRbP=dponrhKTzMKTzMKTuTndxC6SfMXcLLK6ijFVr6jEz.V']
     #driver = webdriver.Chrome(chromepath)
     driver=webdriver.Firefox()
     driver.get(rules[0])
     time.sleep(10)
     # uname = 'ｊｎｖ２７６９１９４８ｇ'
     # password = 'Lx19881210'
     print(rules[4])
     driver.find_element_by_xpath(rules[4]).send_keys(rules[1])  # 你的用户名
     driver.find_element_by_xpath(rules[5]).send_keys(rules[2])
     time.sleep(5)
     driver.find_element_by_xpath(rules[7]).click()
     time.sleep(6)


     # 查询数据子字典
     read = open("D:/test2/智联/zhiLian.txt", 'r')  # 返回一个文件对象
     lines = read.readlines()  # 调用文件的 readline()方法
     read.readable()
     print("---------------------------", address)
     for line in lines:
         if line.find(address) != -1:
             address_no = line.replace(address, '').strip()
             print(address_no)
             break
     read.close()
     #https://rdsearch.zhaopin.com/Home/ResultForCustom?SF_1_1_1=java&SF_1_1_18=548&orderBy=DATE_MODIFIED,1&SF_1_1_27=0&exclude=1
     link =str(rules[8])
     link = link.replace('keyword', word)
     link = link.replace('address_no', address_no)
     print(link)
     #https://rdsearch.zhaopin.com/Home/ResultForCustom?SF_1_1_1=keyword&SF_1_1_18=address_no&orderBy=DATE_MODIFIED,1&pageSize=60&SF_1_1_27=0&exclude=1
     #https://rdsearch.zhaopin.com/Home/ResultForCustom?SF_1_1_1=keyword&SF_1_1_18=address_no&orderBy=DATE_MODIFIED%2C1&SF_1_1_27=0&exclude=1
     #https://rdsearch.zhaopin.com/Home/ResultForCustom?SF_1_1_1=keyword&SF_1_1_18=address_no&orderBy=DATE_MODIFIED%2C1&SF_1_1_27=0&exclude=1
     #https://rdsearch.zhaopin.com/Home/ResultForCustom?SF_1_1_1="+word+"&SF_1_1_18="+address_no+"&orderBy=DATE_MODIFIED%2C1&SF_1_1_27=0&exclude=1"
     driver.get(link)
     time.sleep(5)

     # 当前信息有多少页
     global start_page  # 起始页
     global page_count  # 总页数

     page_index = str(driver.find_element_by_xpath(".//*[@id='rd-resumelist-pageNum']").text)
     nowPag,pageCount = page_index.split("/")
     page_count = int(pageCount)
     print("总页数是=====================")
     print(page_count)
     parse(start_page=1,word=word)

def parse(start_page,word):
        #获取爬取规则


        j = 1
        for i in range(1, 31):
              if rules[11] =="是" :#是否句柄
                    title=rules[9].replace("num",str(j))
                    driver.find_element_by_xpath(title).click()
                    time.sleep(3)
                    # 移动句柄为当前页面
                    all=driver.window_handles
                    z=driver.current_window_handle

                    driver.switch_to_window(driver.window_handles[1])
                    time.sleep(2)
                    ##具体爬取数据的方法
                    auto_info(word)

                    #关闭当前句柄
                    driver.close()
                    #移动句柄
                    driver.switch_to_window(driver.window_handles[0])
                    j = j + 2
                    #print("-----------------------")
              else:
                  auto_info(word)

        #翻页
        if (start_page <= page_count):
           time.sleep(1)
           #html/body/div[6]/div[5]/div/div[3]/button
           #html/body/div[6]/div[5]/div/div[3]/a[3]
           driver.find_element_by_xpath(rules[12]).click()
           time.sleep(5)
           start_page +=1
           print("翻页============================================")

           num1 =start_page
           print(start_page)
           #print(num)

           parse(start_page=num1,word=word)
        else:
            print("-------数据爬取结束---------")


def auto_info(word):
     print("简历内容---------------------------------")
       #简历id
     try:
       s=driver.find_elements_by_xpath(rules[10])
       ids=str(driver.find_element_by_xpath(".//*[@id='resumeContentHead']/div[3]/div/div/div[1]/span").text)
       id,txt_name= ids.split(":")
       path = "D:/test2/智联简历库/"+address+"/"+word+"/"
       #创建目录
       if not os.path.exists(path):
         os.makedirs(path)
       path += txt_name
       path +=".txt"
       print(path)
       f = open(path, 'a')
       for tag in driver.find_elements_by_xpath(rules[10]):#".//*[@id='resumeContentBody']/div"
           print(tag.text)
           try:
            f.write(tag.text)
            f.write("\n")
           except:
               continue
       f.close()
     except:
         pass

@route('/zhiLian/<kyword>/<addre>')#word简历搜索的关键字
def index(kyword,addre):
    global address
    global word
    address = str(addre)
    word =str(kyword)
    login()
    return bottle.template('welcome {{name}}！！', name=word)
run(port=8080, host='localhost')