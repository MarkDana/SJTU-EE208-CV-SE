# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import json

browser=webdriver.Chrome()#加载浏览器；实际使用phantomjs无界面浏览器
with open('lofter.json','r',encoding='utf-8') as f:
    listCookies=json.loads(f.read())
print(listCookies)#这里储存了我的登录信息

try:
    with open('lofterindex.txt','w',encoding='utf-8') as f:
        browser.get("http://www.lofter.com/view")

        for c in listCookies:
            browser.add_cookie(c)#在当前目录下添加登录cookie，以登录
        browser.refresh()#刷新，完成登录
        time.sleep(5)

        image=browser.find_element_by_xpath('//img[@onload="loft.m.lview.g.onImageLoaded(this)"]')#页面中使用js打开的第一张图片
        image.click()
        while(True):#点击“下一张”
            print("_________________________")
            big_img=browser.find_element_by_xpath("//img[contains(@onclick,'loft.x.stopEvent(event);loft.m.lview.g.photoshow')]")
            f.write(big_img.get_attribute('src'))
            print(big_img.get_attribute('src'))
            f.write('\t')
            tags=browser.find_elements_by_xpath("//a[contains(@href,'lofter.com/tag')]")
            for tag in tags:
                str=tag.text.strip('\n')
                f.write(str+'\t')
                print(str)
            f.write('\n')

            #next_button=browser.find_element_by_xpath("//a[contains(@a,'')]"）
            time.sleep(3)#目前使用time.sleep()拖延时间，实际用expected_conditions配合WebDriverWait等待加载完毕
            browser.find_element_by_xpath("//a[@id='next']").click()

finally:
    browser.close()
