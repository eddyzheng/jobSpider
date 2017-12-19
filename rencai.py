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
    #global content
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

#中华人才热线
def login():
     sql = 'select * from spider_base_info_v where w_name="中国人才热线" limit 1'
     global rules
     rules = rule_mysql(sql)
     print(rules)
     #先进行登录
     global driver
     #start_urls = ['http://www.cjol.com/hr/']
     driver = webdriver.Firefox()
     driver.get(rules[0])
     # uname = 'ZHISHENSHUJU'
     # password = 'zs123123'
     #识别验证码
     code = auto_img()
     driver.find_element_by_xpath(rules[4]).send_keys(rules[1])  # 你的用户名
     driver.find_element_by_xpath(rules[5]).send_keys(rules[2])
     #.//*[@id='ValidateCode']
     driver.find_element_by_xpath(rules[6]).send_keys(code)
     time.sleep(10)
     driver.find_element_by_xpath(rules[7]).click()
     time.sleep(5)
     driver.get(rules[8])
     time.sleep(3)
     driver.find_element_by_xpath(rules[14]).click()  # 搜索职位
     driver.find_element_by_xpath(rules[15]).clear()
     driver.find_element_by_xpath(rules[15]).send_keys(keyWord)
     driver.find_element_by_xpath(rules[16]).click()
     time.sleep(3)
     parse()

def parse():
        # #获取爬取规则
        # sql = "SELECT t.title,t.content FROM zhi_lian_RULE t"
        # rule_mysql(sql)
        #j = 1
        for i in range(1, 21):
            if rules[11] =='是':
                 try:#.//*[@id='div_search_list_tbody']/div[1]/ul/li[2]/a
                     #.//*[@id='div_search_list_tbody']/div[num]/ul/li[2]/a
                    title=rules[9]
                    title=title.replace('num',str(i))
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
     path ="D:/test2/中国人才热线简历库/"+keyWord+"/"
     txt_name = driver.find_element_by_xpath(".//*[@id='div_resume']/div/table[2]/tbody/tr[1]/td[2]").text
     print(txt_name)
     if  not os.path.exists(path):
         os.makedirs(path)
     path += txt_name
     path +=".txt"
     print(path)
     content = driver.find_element_by_xpath(rules[10]).text
     print(content)
     f = open(path, 'w')
     f.write(content)
     f.write("\n")
     f.close()
     #print(work_position)
def auto_img():
    driver.get_screenshot_as_file("D:/test2/中国人才热线验证码/img.jpg")
    imgelement = driver.find_element_by_xpath('.//*[@id="validatecodePicture_layer"]')  # 定位验证码
    location = imgelement.location  # 获取验证码x,y轴坐标
    size = imgelement.size  # 获取验证码的长宽
    rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
              int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
    i = Image.open("D:/test2/中国人才热线验证码/img.jpg")  # 打开截图
    i = i.convert('RGB')
    frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
    frame4.save('D:/test2/中国人才热线验证码/new.jpg')
    qq = Image.open('D:/test2/中国人才热线验证码/new.jpg')

    imgry = qq.convert('L')  # 图像加强，二值化
    sharpness = ImageEnhance.Contrast(imgry)  # 对比度增强
    sharp_img = sharpness.enhance(2.0)
    sharp_img.save("D:/test2/中国人才热线验证码/new1.jpg")
    new2 = Image.open('D:/test2/中国人才热线验证码/new1.jpg')
    code = pytesseract.image_to_string(new2,lang='renCai').strip()
    print(code)
    return code
#address='西安'
# keyWord='java'
# login()
@route('/renCai/<keyW>')#word简历搜索的关键字
def index(keyW):
    global keyWord
    keyWord=str(keyW)
    login()
    return bottle.template('welcome {{name}}！！', name=keyWord)
run(port=8080, host='localhost')