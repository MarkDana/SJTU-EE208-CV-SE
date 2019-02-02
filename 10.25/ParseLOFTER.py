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

import sys
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl

ssl._create_default_https_context = ssl._create_unverified_context

class MyWebBrowser(QWebEnginePage):
    app = None
    # 类变量 QApplication
    # 实际测试时，若调用了多个MyWebBrowser对象（有先后顺序的调用）
    # 比如现在某些页面上，获取了所有包含图片的页面链接，再去打开这些链接上抓取图片
    # 容易在这一步 super().__init__() 异常崩溃
    # 可能是在 QApplication.quit()调用时，出现了资源释放异常
    # 改成类变量控制后，没有出现崩溃现象，这个还需要再测试测试

    def __init__(self):
        if MyWebBrowser.app is None:
            MyWebBrowser.app = QApplication(sys.argv)
        # self.app = QApplication(sys.argv)
        # print("DownloadDynamicPage")
        super().__init__()
        self.html = ''
        # 将加载完成信号与槽连接
        self.loadFinished.connect(self._on_load_finished)
        # print("DownloadDynamicPage Init")

    def downloadHtml(self, url):
        """
            将url传入，下载此url的完整HTML内容（包含js执行之后的内容）
            貌似5.10.1自带一个download函数
            这个在5.8.2上也是测试通过的
        :param url:
        :return: html
        """
        self.load(QUrl(url))
        print("\nDownloadDynamicPage", url)
        # self.app.exec_()
        # 函数会阻塞在这，直到网络加载完成，调用了quit()方法，然后就返回html
        MyWebBrowser.app.exec_()
        return self.html

    def _on_load_finished(self):
        """
            加载完成信号的槽
        :return:
        """
        self.html = self.toHtml(self.Callable)

    def Callable(self, html_str):
        """
            回调函数
        :param html_str:
        :return:
        """
        self.html = html_str
        MyWebBrowser.app.quit()
        # self.app.quit()
        
def useWebEngineMethod(url):
    """
        使用PyQt5的网页组件下载完整的动态网页
    """

    webBrowser = MyWebBrowser()
    content = webBrowser.downloadHtml(url)
    f = open('test.html','wb')
    f.write(content)
    #将网页存入文件
    f.close()


def login(url):

    ck="含有个人登录信息，此处略去"
    header={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36','Cookie':ck}
    rq=urllib.request.Request(url,headers=header)
    try:
        content=urllib.request.urlopen(rq,timeout=1).read()
        return content
    except:
        print("FAILED WHEN OPENING "+url)
        pass


def add_page_to_folder(url): #将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    content=login(url)
    f = open('/Users/markdana/Downloads/test.html','wb')

    f.write(content)
    #将网页存入文件
    f.close()

add_page_to_folder('http://www.lofter.com/view')
useWebEngineMethod('http://www.lofter.com/view')
