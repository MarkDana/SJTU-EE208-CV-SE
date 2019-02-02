import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

def gradient(img):#返回img图像的梯度强度图
    img=img.astype(np.float)#否则像素相加减会超过255范围
    res=np.zeros([img.shape[0]-2,img.shape[1]-2],float)
    for i in range(res.shape[0]):
        for j in range(res.shape[1]):
            res[i][j]=math.sqrt(math.pow(img[i+1][j+2]-img[i+1][j],2)+math.pow(img[i+2][j+1]-img[i][j+1],2))
    return res

img1=cv2.imread("/Users/markdana/Desktop/学在交大/电工导/实验作业/上机实验10-图像特征提取实验/图像特征提取实验/images/img1.png",cv2.IMREAD_GRAYSCALE)
img2=cv2.imread("/Users/markdana/Desktop/学在交大/电工导/实验作业/上机实验10-图像特征提取实验/图像特征提取实验/images/img2.png",cv2.IMREAD_GRAYSCALE)

'''
ax1 = plt.subplot(1,2,1)
ax1.hist(img1.ravel(),normed=True, bins=50, color='gray')
ax1.set_title("img1 gray")

ax2 = plt.subplot(1,2,2)
ax2.hist(img2.ravel(),normed=True, bins=50, color='gray')
ax2.set_title("img2 gray")

'''

ax1 = plt.subplot(1,2,1)
ax1.hist(gradient(img1).ravel(),normed=True, bins=50, color='gray')
ax1.set_title("img1 gradient")

ax2 = plt.subplot(1,2,2)
ax2.hist(gradient(img2).ravel(),normed=True, bins=50, color='gray')
ax2.set_title("img2 gradient")

plt.tight_layout()
plt.show()
