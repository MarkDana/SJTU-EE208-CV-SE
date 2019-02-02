# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib.request
import urllib.parse
import os
import urllib
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

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

def union_dfs(a,b):
    for e in b:
        if e not in a:
            a.append(e)

def union_bfs(a,b):
    for  e in b:
        if e not in a:
            a.insert(0,e)

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

def crawl(seed, method, max_page):
    tocrawl = [seed]
    crawled = []
    graph = {}
    while (tocrawl and len(crawled)<max_page):#终止条件：tocrawl为空或者crawed的url数量到了max
        url = tocrawl.pop()
        if url not in crawled:
            print (url)
            content = get_page(url)
            if (content!=None):#防止打不开的超链接（如javascript类）添乱
                add_page_to_folder(url, content)
                outlinks = get_all_links(content, url)
                graph[url]=outlinks
                globals()['union_%s' % method](tocrawl, outlinks)
                crawled.append(url)
    return graph, crawled

if __name__ == '__main__':

    seed = 'http://www.sjtu.edu.cn'
    method = 'bfs'
    max_page = 200

    graph, crawled = crawl(seed, method, max_page)
    for x in crawled :
        print(x)
    print(graph)
