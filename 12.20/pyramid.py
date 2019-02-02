import numpy as np
import cv2
import math

def getIMGpyramid(img):
    res=[img]
    M=img.shape[0]
    N=img.shape[1]
    minMN=min(M,N)
    maxMN=max(M,N)
    while minMN>=315:
        nxt=cv2.resize(res[-1],(0,0),fx=0.8,fy=0.8)
        res.append(nxt)
        M=res[-1].shape[0]
        N=res[-1].shape[1]
        minMN=min(M,N)
    while maxMN<=960:
        nxt=cv2.resize(res[0],(0,0),fx=1.25,fy=1.25)
        res.insert(0,nxt)
        M=res[0].shape[0]
        N=res[0].shape[1]
        maxMN=max(M, N)
    return res

def getLaps(img,s=1.6,k=sqrt(2)):
    L5 = cv2.GaussianBlur(img,(5,5),s*(k**4))#Laplace of Gaussian Layers
    L4 = cv2.GaussianBlur(img,(5,5),s*(k**3))
    L3 = cv2.GaussianBlur(img,(5,5),s*(k**2))
    L2 = cv2.GaussianBlur(img,(5,5),s*k)
    L1 = cv2.GaussianBlur(img,(5,5),s)
    return L5,L4,L3,L2,L1

def getDogs(L5,L4,L3,L2,L1):
    DOG4 = array(L5-L4)#Difference of Gaussian layers
    DOG3 = array(L4-L3)
    DOG2 = array(L3-L2)
    DOG1 = array(L2-L1)
    return DOG1,DOG2,DOG3,DOG4

def findExt(up,src,low):#respectively upper, itself, lower dog layers
    corExts=[]
    for i in range(1,src.shape[0]):
        for j in range(1,src.shape[1]):
            cmp=(src[i-1][j+1],src[i][j+1],src[i+1][j+1],src[i-1][j],src[i+1][j],src[i-1][j-1],src[i][j-1],src[i+1][j-1],
   					up[i-1][j+1],up[i][j+1],up[i+1][j+1],up[i-1][j],up[i][j],up[i+1][j],up[i-1][j-1],up[i][j-1],up[i+1][j-1],
   					low[i-1][j+1],low[i][j+1],low[i+1][j+1],low[i-1][j],low[i][j],low[i+1][j],low[i-1][j-1],low[i][j-1],low[i+1][j-1])

            if max(cmp)<src[i][j] or min(cmp)>src[i][j]:
                corExts.append([i,j])
    return corExts

def EliminateEdge(corExts,src):#src is the middle dog layer
    keyExts=[]
    for i in range(len(corExts)):
        x=corExts[i][0]
        y=corExts[i][1]
        rx,ry=x+1,y+1
        if src[rx][ry]==0:
            continue
        if rx+1<src.shape[0] and ry+1<src.shape[1]:
            fxx=src[rx-1][ry]+src[rx+1,ry]-2*src[rx,ry]
            fyy=src[rx][ry-1]+src[rx,ry+1]-2*src[rx,ry]
            fxy=src[rx-1][ry-1]+src[rx+1][ry+1]-src[rx-1][ry+1]-src[rx+1][ry-1]
            trace=fxx+fyy #for Hessian matrix
            det=fxx*fyy-fxy*fxy
            if trace*trace/det>=12.1: #let ro=10
                keyExts.append(corExts[i])
    return keyExts





