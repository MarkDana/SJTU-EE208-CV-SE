import urllib.request
import ssl
import sys
from bs4 import BeautifulSoup
import re
ssl._create_default_https_context = ssl._create_unverified_context

def parseQiushibaikepic(data):
    soup=BeautifulSoup(data,"lxml")
    docs={}

    whole=soup.findAll('a',{'href':re.compile('^/article')})
    for onePic in whole:
        imgurl='none'
        tmp1=onePic.get('href')
        reg=re.compile(r"(?<=/)\d+")
        match=reg.search(tmp1)
        qs_tag=match.group(0)
        #print(qs_tag)
        tmp2=onePic.find('span')
        if tmp2!=None:#是内容部分
            content=tmp2.string
            if content!=None:
                docs[qs_tag]={'content': content, 'imgurl': imgurl}
        else:#是图片网址部分
            tmp3=onePic.find('img')
            if tmp3!=None:
                relative=tmp3.get('src')
                imgurl="https:"+relative
                docs[qs_tag]['imgurl']=imgurl

    nextpage_rela=soup.findAll('a',{'href':re.compile('^/pic/page/2')})[0].get('href')
    nextpage="https://www.qiushibaike.com"+nextpage_rela


    return docs,nextpage

def write_outputs(results,filename):
    with open(filename, 'w') as f:
        bigdic=results[0]
        nextpage=results[1]
        for key in bigdic:
            onepic=bigdic[key]
            print(onepic)#for test
            f.write(onepic['imgurl']+'\t')
            f.write(onepic['content']+'\n')
        print("\nnext page is: "+str(nextpage))#for test
        f.write("\nnext page is: "+str(nextpage))

def main():
    url='http://www.qiushibaike.com/pic/'
    if len(sys.argv) > 1:
        url = sys.argv[1]
    header={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    rq=urllib.request.Request(url,headers=header)
    data=urllib.request.urlopen(rq).read()

    results = parseQiushibaikepic(data)
    write_outputs(results,'/Users/markdana/Desktop/res3.txt')

if __name__ == '__main__':
    main()
