#coding=utf-8
#!/usr/bin/env python

import sys, os, lucene
import jieba
import bs4
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause
import web
import json
from web import form
from web.net import htmlquote
import os,re
import initvm

urls = ('/', 'search_text',
        '/im','search_img',
        '/s', 'text',
        '/i','img',
        '/jt','jsontext',
        '/ji','jsonimg'
        )
render = web.template.render('templates/') # your templates
login = form.Form(form.Textbox('keyword'),form.Button('Search'),)

def parseCommand(command):
    allowed_opt = ['site']
    command_dict = {}
    opt = 'contents'
    contentTogether=[]
    for i in command.split(' '):
        if ':' in i:
            opt, value = i.split(':')[:2]
            opt = opt.lower()
            if opt in allowed_opt and value != '':
                #command_dict['site'] = command_dict.get('site','')+' '+value#可能一个opt有多个key,但这里对于site，不考虑
                command_dict['site'] = value
        else:
            contentTogether.append(i)#对于site，也不考虑出现空格，则不带':'的都是内容关键词
    contentCommand=' '.join(contentTogether)
    contentCommand=' '.join(jieba.cut(contentCommand))
    command_dict['contents'] = contentCommand
    return command_dict

def SearchTextCommand(command):
    initvm.vm_env.attachCurrentThread()

    STORE_DIR = "textindex"
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

    command_dict = parseCommand(command)
    contentCommand=command_dict['contents'].split(' ')#一个list 里面装了分词后的词语
    querys = BooleanQuery()
    for k,v in command_dict.iteritems():
        query = QueryParser(Version.LUCENE_CURRENT,k,analyzer).parse(v)
        querys.add(query,BooleanClause.Occur.MUST)
    scoreDocs = searcher.search(querys,50).scoreDocs

    finalDocTitles=[]
    finalDocs=[]
    for i, scoreDoc in enumerate(scoreDocs):
        doc = searcher.doc(scoreDoc.doc)
        if(doc.get("title") not in finalDocTitles):
            oneDic={}
            oneDic['url']=doc.get("url")
            oneDic['title']=doc.get("title")
            oneDic['score']=scoreDoc.score

            path=doc.get('path')#html文件夹太大未上传，故文本搜索在助教电脑上无法执行
            file = open(path)
            contents = file.read()
            soup = bs4.BeautifulSoup(contents,features="html.parser")
            contents = ''.join(soup.findAll(text=True))
            file.close()
            allcontentlist=[]

            for oneContent in contentCommand:
                wordlen=len(oneContent)
                contentlist=[i.start() for i in re.finditer(oneContent, contents)]
                for location in contentlist:
                    if(location>20):
                        allcontentlist.append((location,wordlen))
            allcontentlist.sort(key= lambda k:k[0])

            maxlen=min(len(allcontentlist),10)
            contentStr=""
            for i in range(maxlen):
                location=allcontentlist[i]
                for i in range(location[0]-10,location[0]):
                    if (contents[i]!=' 'and contents[i]!='\n' and contents[i]!='\t'):
                        contentStr+=contents[i]
                contentStr+='<font color="red">'
                for i in range(location[0],location[0]+location[1]):
                    contentStr+=contents[i]
                contentStr+='</font>'
                for i in range(location[0]+location[1],location[0]+location[1]+10):
                    if (contents[i]!=' 'and contents[i]!='\n' and contents[i]!='\t'):
                        contentStr+=contents[i]
            oneDic['content']=contentStr
            finalDocTitles.append(doc.get("title"))
            finalDocs.append(oneDic)
    return finalDocs

def SearchImgCommand(command):
    initvm.vm_env.attachCurrentThread()

    STORE_DIR = "jdindex"
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

    contentCommand=' '.join(jieba.cut(command))
    query = QueryParser(Version.LUCENE_CURRENT, "contents", analyzer).parse(contentCommand)
    scoreDocs = searcher.search(query,50).scoreDocs

    Already=[]
    finalDocs=[]
    for i, scoreDoc in enumerate(scoreDocs):
        doc = searcher.doc(scoreDoc.doc)
        itemurl=doc.get("itemurl")
        if itemurl not in Already:
            oneDoc={}
            oneDoc['imgurl']=doc.get("imgurl")
            oneDoc['title']=doc.get("title").strip('\n')
            oneDoc['itemurl']=itemurl
            oneDoc['score']=scoreDoc.score
            finalDocs.append(oneDoc)
            Already.append(itemurl)

    return finalDocs

class search_text:
    def GET(self):
        f = login()
        return render.search_text(f)

class search_img:
    def GET(self):
        f = login()
        return render.search_img(f)

class text:
    def GET(self):
        user_data = web.input()
        keyword=user_data.keyword
        finalDocs = SearchTextCommand(keyword)
        f=login()
        return render.text(f,keyword,finalDocs)

class img:
    def GET(self):
        user_data = web.input()
        keyword=user_data.keyword
        finalDocs = SearchImgCommand(keyword)
        f=login()
        return render.img(f,keyword,finalDocs)

class jsontext:
    def GET(self):
        command=web.input().command.encode('utf-8')
        initvm.vm_env.attachCurrentThread()

        STORE_DIR = "textindex"
        directory = SimpleFSDirectory(File(STORE_DIR))
        searcher = IndexSearcher(DirectoryReader.open(directory))
        analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

        query = QueryParser(Version.LUCENE_CURRENT, "contents", analyzer).parse(command)
        scoreDocs = searcher.search(query,20).scoreDocs

        finalDocs=[]
        for i, scoreDoc in enumerate(scoreDocs):
            doc = searcher.doc(scoreDoc.doc)
            title=doc.get("title")
            if title not in finalDocs:
                finalDocs.append(doc.get("title"))

        web.header('content-type','text/json')
        data={}
        data['q']=command
        data['p']='false'
        data['s']=finalDocs
        return  'fn('+json.dumps(data)+');'

class jsonimg:
    def GET(self):
        command=web.input().command.encode('utf-8')
        initvm.vm_env.attachCurrentThread()

        STORE_DIR = "jdindex"
        directory = SimpleFSDirectory(File(STORE_DIR))
        searcher = IndexSearcher(DirectoryReader.open(directory))
        analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

        query = QueryParser(Version.LUCENE_CURRENT, "contents", analyzer).parse(command)
        scoreDocs = searcher.search(query,20).scoreDocs

        finalDocs=[]
        for i, scoreDoc in enumerate(scoreDocs):
            doc = searcher.doc(scoreDoc.doc)
            title=doc.get("title").strip('\n')
            if title not in finalDocs:
                finalDocs.append(title)

        web.header('content-type','text/json')
        data={}
        data['q']=command
        data['p']='false'
        data['s']=finalDocs
        return  'fn('+json.dumps(data)+');'

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()



