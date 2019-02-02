# -*- coding:utf-8 -*-#
import threading
from queue import Queue
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib.request
import urllib.parse
import os
import urllib
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class Bitarray:
    def __init__(self, size):
        """ Create a bit array of a specific size """
        self.size = size
        self.bitarray = bytearray(size//8+1)

    def set(self, n):
        """ Sets the nth element of the bitarray """
        index = n//8
        position = n % 8
        self.bitarray[index] = self.bitarray[index] | 1 << (7 - position)

    def get(self, n):
        """ Gets the nth element of the bitarray """
        index = n//8
        position = n % 8
        return (self.bitarray[index] & (1 << (7 - position))) > 0

m=1000000#max_size<m/20即可
k=10
bitarray_obj = Bitarray(m)
q=Queue()
varLock = threading.Lock()
graph={}
count=0
max_page=0

def BKDRHash(key,k,m):#参数有k、m，返回数组
    seeds=[31,131,1313,13131,131313,1313131,13131313,131313131,1313131313,13131313131]#31 131 1313 13131 131313 etc..
    hash_res = []
    for i in range(k):
        seed=seeds[i]
        hash=0
        for j in range(len(key)):
            hash=(hash*seed)+ord(key[j])
            hash=hash%m
        hash_res.append(hash)
    return hash_res



def page_not_in_crawled(page):
    flag=0
    hash_res=BKDRHash(page,k,m)
    for i in hash_res:
        if(bitarray_obj.get(i)==0):
            flag=1
            break
    return flag

def add_to_crawled(page):
    #page=valid_filename(page)
    hash_res=BKDRHash(page,k,m)
    for i in hash_res:
        bitarray_obj.set(i)
    global  count
    count+=1
    print(count)

def working():
    global count,max_page

    while (count<=max_page):
        page=q.get()
        if page_not_in_crawled(page):
            print(page)
            content=get_page(page)
            if(content!=None):
                add_page_to_folder(page,content)
                outlinks=get_all_links(content,page)
                for link in outlinks:
                    q.put(link)
                if varLock.acquire():
                    graph[page]=outlinks
                    add_to_crawled(page)
                    varLock.release()
            q.task_done()

    while 1:
        q.task_done()

def valid_filename(s):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s

def get_page(url):
    header={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    rq=urllib.request.Request(url,headers=header)
    try:
        content=urllib.request.urlopen(rq,timeout=1).read()
        return content
    except:
        print("FAILED WHEN OPENING "+url)
        pass

def get_all_links(content, url):
    links = []
    soup=BeautifulSoup(content,"lxml")
    t1=soup.findAll('a')
    for t2 in t1:
        t3=t2.get('href')
        complete_link=urljoin(url,t3)
        if complete_link not in links:
            links.append(complete_link)
    return links



def add_page_to_folder(url, content): #将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    index_filename = '/Users/markdana/Desktop/index.txt'    #index.txt中每行是'网址 对应的文件名'
    folder = '/Users/markdana/Desktop/html'                 #存放网页的文件夹
    filename = valid_filename(url) #将网址变成合法的文件名
    index = open(index_filename, 'a')
    index.write(url + '\t' + filename + '\n')
    index.close()
    if not os.path.exists(folder):  #如果文件夹不存在则新建
        os.mkdir(folder)
    f = open(os.path.join(folder,filename+'.html'), 'wb')#储存为html文件较好
    f.write(content)               #将网页存入文件
    f.close()

def crawl(seed, NUM):
    q.put(seed)
    for i in range(NUM):
        t = threading.Thread(target=working)
        t.setDaemon(True)
        t.start()
    q.join()


if __name__ == '__main__':

    seed = 'http://www.sjtu.edu.cn'
    NUM=20
    max_page = 300
    m=20*max_page
    bitarray_obj = Bitarray(m)
    start=time.time()
    crawl(seed, NUM)
    end=time.time()
    print(end-start)

