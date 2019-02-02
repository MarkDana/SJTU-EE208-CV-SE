import numpy as np
import cv2
import math

def getGrad(img):
    img=cv2.GaussianBlur(img,(7,7),1.0)*1.0
    cannyX = np.array([[-3,-10,-3],
                            [0,0,0],
                            [3,10,3]])
    cannyY = np.array([[-3,0,3],
                            [-10,0,10],
                            [-3,0,3]])
    grad_x=cv2.filter2D(img,ddepth=-1,kernel=cannyX,anchor=(-1,-1))
    grad_y=cv2.filter2D(img,ddepth=-1,kernel=cannyY,anchor=(-1,-1))

    gradMag=np.hypot(grad_x,grad_y)
    gradAng=np.arctan2(grad_y,np.add(grad_x,0.0000001))*180/np.pi
    for x in range(gradAng.shape[0]):
        for y in range(gradAng.shape[1]):
            if gradAng[x,y]<0:gradAng[x,y]+=360
    return gradMag,gradAng

def findOri(gradMag,gradAng,corners):
    oriList=[]
    for corner in corners:
        x=int(corner[0][1])
        y=int(corner[0][0])
        hist=np.zeros(36,dtype=float)
        try:
            subMag=np.array(gradMag[x-8:x+8,y-8:y+8])
            subAng=np.array(gradAng[x-8:x+8,y-8:y+8])
            for i in range(16):
                for j in range(16):
                    mag=subMag[i,j]
                    ang=subAng[i,j]
                    hist[int(ang/10)]+=mag#分成36份,且排除掉边界
        except:continue
        mainOri=np.where(hist==np.max(hist))[0][0]*10
        oriList.append([x,y,mainOri])
    return oriList

def rotateCoor(x,y,mainOri,detx,dety):#物体坐标系内经过detx,dety后的点的图像坐标系坐标,可能越界,后面要检查
    r=math.hypot(detx,dety)
    detAng=mainOri+math.atan2(dety,detx+0.0000001)*180.0/math.pi
    if detAng<0:detAng+=360.0
    if detAng>360:detAng-=360.0
    newx=x*1.0+r*math.cos(detAng/180.0*math.pi)
    newy=y*1.0+r*math.sin(detAng/180.0*math.pi)
    return newx,newy

def findAllSift(img,gradMag,gradAng,oriList):
    kps,des=[],[]
    for key in oriList:
        x,y,mainOri=key[0],key[1],key[2]
        oneSift=[]
        xstarts=[-8,-4,0,4]
        ystarts=[-8,-4,0,4]
        for xstart in xstarts:
            for ystart in ystarts:
                hist=[0.0]*8
                for i in range(4):
                    for j in range(4):
                        detx,dety=xstart+i,ystart+j
                        newx,newy=rotateCoor(x,y,mainOri,detx,dety)
                        if newx<0 or newy<0 or newx>img.shape[0]-2 or newy>img.shape[1]-2:
                            continue
                        intx,inty=int(newx),int(newy)
                        dx1,dx2,dy1,dy2=newx-intx,1+intx-newx,newy-inty,inty+1-newy
                        ang=gradAng[intx,inty]*dx2*dy2+gradAng[intx+1,inty]*dx1*dy2+gradAng[intx,inty+1]*dx2*dy1+gradAng[intx+1,inty+1]*dx1*dy1
                        ang-=mainOri
                        if ang<0:ang+=360.0
                        pixel=img[intx,inty]*dx2*dy2+img[intx+1,inty]*dx1*dy2+img[intx,inty+1]*dx2*dy1+img[intx+1,inty+1]*dx1*dy1
                        #pixel=gradMag[intx,inty]*dx2*dy2+gradMag[intx+1,inty]*dx1*dy2+gradMag[intx,inty+1]*dx2*dy1+gradMag[intx+1,inty+1]*dx1*dy1
                        hist[int(ang/45)]+=pixel
                oneSift+=hist
        sum=0.0
        for value in oneSift:
            sum+=value**2
        if sum!=0:oneSift=np.array(oneSift)/math.sqrt(sum)
        des.append(oneSift)
        kps.append(cv2.KeyPoint(y,x,_size=gradMag[x,y]))
    return kps,np.array(des,dtype=np.float32)

def drawMatches(img1_dir,img2_dir,maxMatches=50):
    img1=cv2.imread(img1_dir,cv2.IMREAD_GRAYSCALE)
    img2=cv2.imread(img2_dir,cv2.IMREAD_GRAYSCALE)

    gradMag1,gradAng1=getGrad(img1)
    gradMag2,gradAng2=getGrad(img2)

    colorimg1=cv2.imread(img1_dir,cv2.IMREAD_COLOR)
    colorimg2=cv2.imread(img2_dir,cv2.IMREAD_COLOR)

    corners1=cv2.goodFeaturesToTrack(img1,maxCorners=maxMatches,qualityLevel=0.01,minDistance=10,blockSize=3,k=0.04)
    corners2=cv2.goodFeaturesToTrack(img2,maxCorners=maxMatches,qualityLevel=0.01,minDistance=10,blockSize=3,k=0.04)

    kps1,des1=findAllSift(img1,gradMag1,gradAng1,findOri(gradMag1,gradAng1,corners1))
    kps2,des2=findAllSift(img2,gradMag2,gradAng2,findOri(gradMag2,gradAng2,corners2))

    bf=cv2.BFMatcher()
    matches=bf.knnMatch(des1,des2,k=2)
    nice_match=[]
    for m,n in matches:
        if m.distance<0.85*n.distance:
            nice_match.append([m])
    M=max(colorimg1.shape[0],colorimg2.shape[0])
    N=colorimg1.shape[1]+colorimg2.shape[1]
    img_match=np.zeros((M, N))
    img_match=cv2.drawMatchesKnn(colorimg1,kps1,colorimg2,kps2,
        nice_match, img_match, matchColor=[0,0,255], singlePointColor=[255,0,0])
    cv2.imshow("Matched KeyPoints", img_match)
    cv2.waitKey(0)

img1_dir='../target.jpg'
img2_dir='../dataset/3.jpg'
drawMatches(img1_dir,img2_dir,maxMatches=200)










