# coding:utf8

from selenium import webdriver
import data_outputer
import re
import time

def CET_spider(i,xm):
    try:
        # 引入phantomjs.exe
        driver = webdriver.PhantomJS(executable_path='D:\phantomjs.exe')
        url = "http://www.chsi.com.cn/cet/query"
        i = str(i)
        driver.get(url)
        driver.find_element_by_id('zkzh').send_keys(i)
        driver.find_element_by_id('xm').send_keys(xm)
        driver.find_elements_by_tag_name('form')[1].submit()
        driver.set_page_load_timeout(10)
        all = driver.find_element_by_class_name("colorRed").text
        print all
        scoreblock = driver.find_element_by_xpath("//tr[6]/td[1]").text
        scoreblock = str(scoreblock.encode("utf-8"))
        # print scoreblock
        m = re.findall(r'(\w*[0-9]+)\w*', scoreblock)
        # print m
        driver.close()
        # 延时爬取
        time.sleep(10)
        return m[0],m[1],m[2],m[3]
    except:
        print "验证码"


databse = data_outputer.HtmlOutputer()
databse.database_connect()
databse.database_set_charset('itcast')
# 存储有学号和姓名的数据库
students = databse.database_read('stu_user')
total = len(students)
# 开始同学的考场号
room = 0
# 开始同学的座位号
set = 0
# 考场号
i = 420020161100000+room*100+set
print i
for num in range(0, total):
    print "姓名：", students[num][1],
    number = students[num][0].replace('U','')
    real_num = students[num][0]
    print " 学号整数部分", int(number),
    if(CET_spider(i, students[num][1]) == None):
        print "需要验证码"
        if (set == 30):
            room += 1
            set = 1
        else:
            set += 1
        i = 420020161100000 + room * 100 + set
    else:
        score, listen, read, write = CET_spider(i, students[num][1])
        while(score == ''):
            print "有补考生"
            if(set == 30):
                room += 1
                set = 1
            else:
                set += 1
            i = 420020161100000 + room * 100 + set
            score = CET_spider(i, students[num][1])
        print " CET考号：", i, " 分数： ", score, listen, read, write
        sql = "INSERT INTO `stu_cet`(`student_number`, `cet_number`, `score`, `score_listen`, `score_read`, `score_write`) VALUES ('%s',%d,%d,%d,%d,%d)" %(real_num, int(i), int(score),int(listen) ,int(read), int(write))
        databse.database_insert(sql)
        databse.sql_commit()
        print sql
        if (set == 30):
            room += 1
            set = 1
        else:
            set += 1
        i = 420020161100000 + room * 100 + set
