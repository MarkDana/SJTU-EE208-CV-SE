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
from web import form
from web.net import htmlquote
import os,re
import initvmText

urls = ('/', 'index','/s', 's')
render = web.template.render('/Users/markdana/Desktop/templates/') # your templates
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

def func(command):
    initvmText.vm_env.attachCurrentThread()
    command_dict = parseCommand(command)
    contentCommand=command_dict['contents'].split(' ')#一个list 里面装了分词后的词语
    querys = BooleanQuery()
    for k,v in command_dict.iteritems():
        query = QueryParser(Version.LUCENE_CURRENT,k,initvmText.analyzer).parse(v)
        querys.add(query,BooleanClause.Occur.MUST)
    scoreDocs = initvmText.searcher.search(querys,50).scoreDocs

    finalDocTitles=[]
    finalDocs=[]
    for i, scoreDoc in enumerate(scoreDocs):
        doc = initvmText.searcher.doc(scoreDoc.doc)
        if(doc.get("title") not in finalDocTitles):
            oneDic={}
            url=doc.get("url")
            title=doc.get("title")

            strTitle='<a href="'+url+'">'+title+'</a>'
            oneDic['title']=strTitle
            oneDic['score']=scoreDoc.score

            path=doc.get('path')
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

class index:
    def GET(self):
        f = login()
        return render.formtest(f)

class s:
    def GET(self):
        user_data = web.input()
        finalDocs = func(user_data.keyword)
        return render.result(finalDocs)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

