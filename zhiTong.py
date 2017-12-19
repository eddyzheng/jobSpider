# -*- coding: utf-8 -*-
import os
import time

import pymysql
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

#智通
def login():
     sql = 'select * from spider_base_info_v where w_name="智聘通" limit 1'
     global rules
     rules = rule_mysql(sql)
     print(rules)
     #先进行登录
     global driver
     # start_urls = ['http://zp.job5156.com/login/com/']
     driver = webdriver.Firefox()
     driver.get(rules[0])
     #获取验证码
     code=auto_img()
     # uname = 'ZHISHENSHUJU'
     # password = '123.123.ZS'
     driver.find_element_by_xpath(rules[4]).send_keys(rules[1])  # 你的用户名
     driver.find_element_by_xpath(rules[5]).send_keys(rules[2])
     driver.find_element_by_xpath(rules[6]).send_keys(code)

     time.sleep(7)
     driver.find_element_by_xpath(rules[7]).click()
     time.sleep(5)
     #
     read = open("D:/test2/智通图片/zhitong.txt", 'r')  # 返回一个文件对象
     lines = read.readlines()  # 调用文件的 readline()方法
     for line in lines:
         addre = str(address)
         if line.find(addre) != -1:
             address_no = line.replace(addre, '').strip()
             print(address_no)
             break
     read.close()
 #http://zp.job5156.com/s/r/result?keyword=guanjianzi%E5%B7%A5%E7%A8%8B%E5%B8%88&keywordOr=&workareaList=address_no&degreeFrom=1&degreeTo=6&workyearFrom=-1&workyearTo=11&posTypeList=&ageFrom=&ageTo=&gender=&locationList=&updateIn=90&languageLevel=&resumeType=0&comName=&comRecent=&jobName=&jobRecent=&latestIndustry=&name_hometownList=&hometownList=&speciality=&school=&photoExist=&resumeEnExist=
     link =rules[8].replace("guanjianzi",keyWord)
     link =link.replace("address_no",address_no)
     driver.get(link)
     driver.implicitly_wait(10)

     #
     parse()

def parse():
        # #获取爬取规则
        for i in range(3, 22):
            if rules[11] =="是":

                 try:#.//*[@id='js_resSearch']/div[num]/div[2]/h3/a
                    title=rules[9].replace("num",str(i))
                    driver.find_element_by_xpath(title).click()
                    driver.implicitly_wait(7)
                    # 移动句柄为当前页面
                    all=driver.window_handles
                    z=driver.current_window_handle

                    driver.switch_to_window(driver.window_handles[1])
                    ##具体爬取数据的方法
                    auto_info()

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
           parse()
        except:
           driver.quit()
           print("--------------------------爬取简历结束--------------------------")

def auto_info():
     print("简历内容---------------------------------")
     path ="D:/test2/智通网简历库/"+address+"/"+keyWord+"/"
     txt_name = str(driver.find_element_by_xpath("html/body/form/div/div/div[2]/div[2]/table/tbody/tr/td[2]/p[2]").text)
     name,no=txt_name.split("：")
     no = no.strip()
     if  not os.path.exists(path):
         os.makedirs(path)
     path += no
     path +=".txt"
     print(path)
     content = driver.find_element_by_xpath(rules[10]).text
     f = open(path, 'w')
     f.write(content)
     f.write("\n")
     f.close()
     #print(work_position)
def auto_img():
    driver.get_screenshot_as_file("D:/test2/智通图片/img.jpg")
    imgelement = driver.find_element_by_xpath('.//*[@id="captcha_image"]')  # 定位验证码
    location = imgelement.location  # 获取验证码x,y轴坐标
    size = imgelement.size  # 获取验证码的长宽
    rangle = (int(location['x'] + 10), int(location['y']), int(location['x'] + size['width'] - 20),
              int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
    i = Image.open("D:/test2/智通图片/img.jpg")  # 打开截图
    i = i.convert('RGB')
    frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
    frame4.save('D:/test2/智通图片/new.jpg')
    qq = Image.open('D:/test2/智通图片/new.jpg')

    imgry = qq.convert('L')  # 图像加强，二值化
    sharpness = ImageEnhance.Contrast(imgry)  # 对比度增强
    sharp_img = sharpness.enhance(2.0)
    sharp_img.save("D:/test2/智通图片/new1.jpg")
    new2 = Image.open('D:/test2/智通图片/new1.jpg')
    code = pytesseract.image_to_string(new2,lang='zhiTong').strip()
    return code

@route('/zhiTong/<addr>/<keyW>')#word简历搜索的关键字
def index(addr,keyW):
    global address
    global keyWord
    address=str(addr)
    keyWord=str(keyW)
    login()
    return bottle.template('welcome {{name}}！！', name=keyWord)
run(port=8080, host='localhost')