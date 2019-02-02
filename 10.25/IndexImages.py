#coding=utf-8
#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"
import urlparse
import bs4
import jieba
import re
import sys, os, lucene, threading, time
from datetime import datetime

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

"""
This class is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""

class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir))
        analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)
        self.indexDocs(root, writer)
        ticker = Ticker()
        print 'commit index',
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print 'done'

    def indexDocs(self, root, writer):

        t1 = FieldType()
        t1.setIndexed(False)
        t1.setStored(True)
        t1.setTokenized(False)

        t3 = FieldType()
        t3.setIndexed(True)
        t3.setStored(False)
        t3.setTokenized(True)#利用预先设置的analyzer进行分词，这里是根据空格
        t3.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        total=0
        file = open(root,"r")
        for line in file.readlines():
            try:
                imgurl, itemurl, content = line.split('\t')
                total+=1
                print total
                print "adding", content
                contents = ' '.join(jieba.cut(content))
                doc = Document()
                doc.add(Field("imgurl", imgurl, t1))
                doc.add(Field("itemurl", itemurl, t1))
                doc.add(Field("title", content, t1))
                doc.add(Field("contents",contents,t3))
                writer.addDocument(doc)
            except Exception, e:
                    print "Failed in indexDocs:", e
        file.close()

if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    try:
        IndexFiles('jdindex.txt',"jdindex")
        end = datetime.now()
        print end - start
    except Exception, e:
        print "Failed: ", e
        raise e
