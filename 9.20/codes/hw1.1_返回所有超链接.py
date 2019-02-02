import sys
import urllib.request
from bs4 import BeautifulSoup


def parseURL(content):
    urlset = set()
    soup=BeautifulSoup(content,"lxml")
    t1=soup.findAll('a')
    for t2 in t1:
        t3=t2.get('href')
        urlset.add(t3)
    return urlset

def write_outputs(urls,filename):
    with open(filename, 'w') as f:
        for url in urls:
            f.write(url)
            f.write('\n')

def main():
    url = 'http://www.baidu.com'
    if len(sys.argv) > 1:
        url = sys.argv[1]
    content = urllib.request.urlopen(url).read()
    urls = parseURL(content)
    write_outputs(urls,'/Users/markdana/Desktop/res1.txt')

if __name__ == '__main__':
    main()
