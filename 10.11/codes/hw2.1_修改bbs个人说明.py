#!/usr/bin/python
# coding: utf-8
import urllib.request
import urllib.parse
import http.cookiejar
import ssl
from bs4 import BeautifulSoup
ssl._create_default_https_context = ssl._create_unverified_context

def bbs_set(id, pw, text):
    cj = http.cookiejar.CookieJar()	#初始化cookie
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    urllib.request.install_opener(opener)	#将cookie加入opener
    logindata = urllib.parse.urlencode({#根据发出数据模拟request-body
        'id' : '%s'%id,
        'pw' : '%s'%pw,
        'submit' : 'login'
        }).encode('GB2312')

    ua='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    header={'User-Agent':ua}
    req = urllib.request.Request(url = 'https://bbs.sjtu.edu.cn/bbslogin', headers=header, data = logindata)
    urllib.request.urlopen(req) 	#POST方式发出请求,则cookie已创建

    updatedata = urllib.parse.urlencode({	#根据发出数据模拟request-body
        'type': 'update',
        'text': ("%s"%text).encode('GB2312')
        }).encode(encoding='GB2312')
    updaterq=urllib.request.Request(url='https://bbs.sjtu.edu.cn/bbsplan',headers=header,data=updatedata)
    urllib.request.urlopen(updaterq)#更新个人说明
    testrq=urllib.request.Request(url='https://bbs.sjtu.edu.cn/bbsplan')#检查是否已近更新
    testresult=urllib.request.urlopen(testrq).read()
    soup = BeautifulSoup(testresult,"lxml")
    print ("新的个人说明为："+str(soup.find('textarea').string).strip())


if __name__ == '__main__':
    id = 'markdana'
    pw = '123456'
    text = '咕噜sugulutu'
    bbs_set(id, pw, text)
