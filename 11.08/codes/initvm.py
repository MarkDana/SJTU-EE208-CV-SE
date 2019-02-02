INDEX_DIR = "IndexFiles.index"
import lucene
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
vm_env=lucene.initVM(vmargs=['-Djava.awt.headless=true'])


