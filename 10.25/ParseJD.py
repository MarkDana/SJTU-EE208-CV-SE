# -*- coding:utf-8 -*-#
import threading
from queue import Queue
import time
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import urllib
import ssl
import random

ssl._create_default_https_context = ssl._create_unverified_context

q=Queue()
varLock = threading.Lock()
graph={}
count=0
max_page=0

def working():
    global count,max_page

    while (count<=max_page):
        print(count)
        page=q.get()
        content=get_page(page)
        if(content!=None):
            add_page_to_index(page,content)
        if varLock.acquire():
            varLock.release()
        q.task_done()

    while 1:
        q.task_done()

def get_page(url):
    header={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    rq=urllib.request.Request(url,headers=header)
    try:
        content=urllib.request.urlopen(rq,timeout=2).read()
        return content
    except:
        print("FAILED WHEN OPENING "+url)
        pass


def add_page_to_index(url,content):
    global  count
    bs=BeautifulSoup(content,'lxml')
    img=bs.find(id="spec-img")
    if img==None:
        return
    imgurl="https:"+img.get("data-origin")
    if(imgurl!="https:"):
        title=bs.find("title").text
        title=title[:title.find("【行情 报价 价格 评测】-京东")]
        print(title)
        print(imgurl)
        count+=1
        index_filename = 'jdindex.txt'    #index.txt中每行是'网址 对应的文件名'
        index = open(index_filename, 'a')
        index.write(imgurl + '\t' + url+ '\t' + title + '\n')

def crawl(NUM):
    randomlist=[]
    len=0
    while (len<=10*max_page):#先给q初始化，随机生成商品网页
        rd=randomNum(7)
        if(rd not in randomlist):
            url="https://item.jd.com/"+rd+".html"
            q.put(url)
            len+=1
    for i in range(NUM):
        t = threading.Thread(target=working)
        t.setDaemon(True)
        t.start()
    q.join()

def randomNum(digit):
    id = ''.join(str(i) for i in random.sample(range(0,9),digit))
    return id

if __name__ == '__main__':

    NUM=20
    max_page = 10000
    start=time.time()
    crawl(NUM)
    end=time.time()
    print(end-start)

