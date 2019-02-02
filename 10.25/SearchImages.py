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

def run(searcher, analyzer):
    while True:
        print
        print "Hit enter with no input to quit."
        command = raw_input("Query:")
        if command == '':
            return
        print
        print "Searching for:", command

        contentCommand=' '.join(jieba.cut(command))
        query = QueryParser(Version.LUCENE_CURRENT, "contents",  analyzer).parse(contentCommand)
        scoreDocs = searcher.search(query,50).scoreDocs

        for i, scoreDoc in enumerate(scoreDocs):
            doc = searcher.doc(scoreDoc.doc)
            print "图片: ",doc.get("imgurl")
            print "名称: ",doc.get("title").strip('\n')
            print "链接: ",doc.get("itemurl")
            print "相关度: ",scoreDoc.score
            print ""

            # print 'explain:', searcher.explain(query, scoreDoc.doc)
        print "%s total matching documents." % len(scoreDocs)

if __name__ == '__main__':
    STORE_DIR = "jdindex"
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    run(searcher, analyzer)
    del searcher
