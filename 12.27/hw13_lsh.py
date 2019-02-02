import random
import cv2
import os
import json
import numpy as np
import codecs
import time
'''
some so-so seeds
[3, 8, 17, 20]
[3, 11, 13, 20]
[2, 6, 10, 18]
[2, 10, 18, 19]
[1, 6, 15, 18]
[1, 2, 6, 18]
[1, 2, 4, 15]
[4, 6, 15, 19]
'''
def getInt(x):
    if x<=0.32022380752609653:return 0
    if x<=0.33984590482268179:return 1
    return 2

def getFeatureVec(imgdir):
    img=cv2.imread(imgdir,cv2.IMREAD_COLOR)
    FeatureVec=[]
    row,col=img.shape[0],img.shape[1]
    Hset=[img[:row//2,:col//2],img[:row//2,col//2+1:],img[row//2+1:,:col//2],img[row//2+1:,col//2+1:]]
    for quater in Hset:
        imgSum=float(np.sum(quater))
        bgr=[np.sum(quater[:,:,0])/imgSum,np.sum(quater[:,:,1])/imgSum,np.sum(quater[:,:,2])/imgSum]
        quaterRes=[getInt(x) for x in bgr]
        FeatureVec.extend(quaterRes)
    return FeatureVec

class hammingHasher(object):
    def __init__(self, inLength=12,outLength=4,maxUnitValue=2,mySeeds=None):
        if mySeeds:self.hashSeeds=mySeeds
        else:
            self.hashSeeds=random.sample(range(1,inLength*maxUnitValue+1),outLength)
        self.inLength,self.outLength,self.maxUnitValue=inLength,outLength,maxUnitValue

    def hashIndex(self,inVector):
        hashStr=""
        for oneSeed in self.hashSeeds:
            ind=(oneSeed-1)//self.maxUnitValue
            left=oneSeed-ind*self.maxUnitValue
            hashStr+=(str(int(inVector[ind]>=left)))
        return int(hashStr,2)

    def makeHash(self,dataset):
        resList=[]
        for i in range(2**self.outLength):resList.append([])

        for dirpath,dirnames,filenames in os.walk(dataset):
            for file in filenames:
                imgdir=os.path.join(dirpath,file)
                if not imgdir.endswith("jpg"):continue
                featureVec=getFeatureVec(imgdir)
                hashInd=self.hashIndex(featureVec)
                featureStr=' '.join([str(x) for x in featureVec])
                resList[hashInd].append({
                    "img":imgdir,
                    "featureVec":featureStr
                })
        hashData=[{
            "inLength":self.inLength,
            "outLength":self.outLength,
            "maxUnitValue":self.maxUnitValue,
            "hashSeeds":self.hashSeeds
        }]

        storeData=[hashData,resList]
        with codecs.open("./dataset.json",'w')as f:
            json.dump(storeData,f,ensure_ascii=False,indent=4)

class lshTable(object):
    def __init__(self,datadir="dataset.json"):
        with open(datadir,'r') as f:
            storeData=json.load(f)
            hashDataDict,resList=storeData[0][0],storeData[1]
            self.inLength=hashDataDict["inLength"]
            self.outLength=hashDataDict["outLength"]
            self.maxUnitValue=hashDataDict["maxUnitValue"]
            self.hashSeeds=hashDataDict["hashSeeds"]
            self.resList=resList

    def hashIndex(self,inVector):
        hashStr=""
        for oneSeed in self.hashSeeds:
            ind=(oneSeed-1)//self.maxUnitValue
            left=oneSeed-ind*self.maxUnitValue
            hashStr+=(str(int(inVector[ind]>=left)))
        return int(hashStr,2)

    def add(self,imgdir):
        featureVec=getFeatureVec(imgdir)
        hashInd=self.hashIndex(featureVec)
        featureStr=' '.join([str(x) for x in featureVec])
        self.resList[hashInd].append({
                    "img":imgdir,
                    "featureVec":featureStr
                })
        hashData=[{
            "inLength":self.inLength,
            "outLength":self.outLength,
            "maxUnitValue":self.maxUnitValue,
            "hashSeeds":self.hashSeeds
        }]
        storeData=[hashData,self.resList]
        with codecs.open("./dataset.json",'w')as f:
            json.dump(storeData,f,ensure_ascii=False,indent=4)

    def lookup(self,imgdir):
        start=time.clock()
        featureVec=np.array(getFeatureVec(imgdir))
        hashInd=self.hashIndex(featureVec)
        minNow=float("inf")
        possibleMatch=[]
        for toCompare in self.resList[hashInd]:
            vec=np.array([int(x) for x in toCompare["featureVec"].split(' ')])
            euclid=np.linalg.norm(featureVec-vec)
            if(euclid<minNow):
                minNow=euclid
                possibleMatch=[toCompare["img"]]
            elif(euclid==minNow):
                possibleMatch.append(toCompare["img"])
        end=time.clock()
        return possibleMatch,end-start

def searchClumsy(target,dataset):
    orb = cv2.ORB_create()
    tarimg=cv2.imread(target, cv2.IMREAD_GRAYSCALE)
    keypoint1, descriptor1 = orb.detectAndCompute(tarimg, None)
    minDis=float('inf')
    bestMatch=""
    global kp2,nice_match
    start=time.clock()
    for dirpath,dirnames,filenames in os.walk(dataset):
        for file in filenames:
            imgdir=os.path.join(dirpath,file)
            if not imgdir.endswith('jpg'):continue
            toCompare=cv2.imread(imgdir, cv2.IMREAD_GRAYSCALE)
            keypoint2, descriptor2 = orb.detectAndCompute(toCompare, None)
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(descriptor1, descriptor2)
            matchDis=[x.distance for x in matches]
            avgDis=sum(matchDis)/(len(matchDis)+0.0000001)
            if avgDis<minDis:
                minDis=avgDis
                bestMatch=imgdir
                kp2=keypoint2
                nice_match=sorted(matches, key=lambda x: x.distance)
    end=time.clock()
    print("best match:"+bestMatch)
    print("costs %s seconds."%(end-start))
    colorimg1=cv2.imread(target,cv2.IMREAD_COLOR)
    colorimg2=cv2.imread(bestMatch,cv2.IMREAD_COLOR)

    img_match = cv2.drawMatches(colorimg1, keypoint1,colorimg2,kp2,nice_match[:30],colorimg2,flags=2)
    cv2.imwrite('nice_match.jpg',img_match)

if __name__ == '__main__':

    dataset="/Exp12/Dataset"
    target="/Exp12/target.jpg"

    '''
    建立索引
    mySeed=[3, 8, 17, 20]
    h=hammingHasher(mySeeds=mySeed)
    h.makeHash(dataset)
    '''

    lsh=lshTable()
    possibleMatch,cost=lsh.lookup(target)
    print(possibleMatch)
    print("costs %s seconds."%cost)

    '''暴力搜索
    searchClumsy(target,dataset)
    '''

