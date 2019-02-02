import sys
import urllib.request
from bs4 import BeautifulSoup

def parseIMG(content):
    imgset = set()
    soup=BeautifulSoup(content,"lxml")
    t1=soup.findAll('img')
    for t2 in t1:
        t3=t2.get('src')
        imgset.add(t3)

    return imgset

def write_outputs(url,imgs,filename):
    with open(filename, 'w') as f:
        for img in imgs:
            print(img)#test
            f.write(url)
            f.write(str(img)[2:])#to print the absolute address
            #urljoin in urlparse library also works
            f.write('\n')

def main():
    url = 'http://image.baidu.com/imagevippc/'
    if len(sys.argv) > 1:
        url = sys.argv[1]
    content = urllib.request.urlopen(url).read()
    print(content)
    imgs = parseIMG(content)
    write_outputs(url,imgs,'/Users/markdana/Desktop/res2.txt')

if __name__ == '__main__':
    main()


