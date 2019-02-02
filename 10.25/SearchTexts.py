#coding=utf-8
#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene
import jieba
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause

"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""
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

def run(searcher, analyzer):
    while True:
        print
        print "Hit enter with no input to quit."
        command = raw_input("Query:")
        if command == '':
            return
        print
        print "Searching for:", command

        command_dict = parseCommand(command)
        querys = BooleanQuery()
        for k,v in command_dict.iteritems():
            query = QueryParser(Version.LUCENE_CURRENT, k,  analyzer).parse(v)
            querys.add(query,BooleanClause.Occur.MUST)

        scoreDocs = searcher.search(querys,50).scoreDocs
        
        
        finalDocTitles=[]
        for i, scoreDoc in enumerate(scoreDocs):
            doc = searcher.doc(scoreDoc.doc)
            if(doc.get("title") not in finalDocTitles):
                print 'title:', doc.get("title"), 'url:', doc.get("url"), 'score:', scoreDoc.score, 'contents:', doc.get('contents')
                finalDocTitles.append(doc.get("title"))
            # print 'explain:', searcher.explain(query, scoreDoc.doc)
        print "%s total matching documents." % len(finalDocTitles)

if __name__ == '__main__':
    STORE_DIR = "textindex"
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    run(searcher, analyzer)
    del searcher
