import cv2
import numpy as np
import matplotlib.pyplot as plt

img1=cv2.imread("/Users/markdana/Desktop/学在交大/电工导/实验作业/上机实验10-图像特征提取实验/图像特征提取实验/images/img1.png",cv2.IMREAD_COLOR)
img2=cv2.imread("/Users/markdana/Desktop/学在交大/电工导/实验作业/上机实验10-图像特征提取实验/图像特征提取实验/images/img2.png",cv2.IMREAD_COLOR)

img1_b=np.sum(img1[:,:,0])
img1_g=np.sum(img1[:,:,1])
img1_r=np.sum(img1[:,:,2])
total1=img1_b+img1_g+img1_r
img1_b=float(img1_b)/total1
img1_g=float(img1_g)/total1
img1_r=float(img1_r)/total1

img2_b=np.sum(img2[:,:,0])
img2_g=np.sum(img2[:,:,1])
img2_r=np.sum(img2[:,:,2])
total2=img2_b+img2_g+img2_r
img2_b=float(img2_b)/total2
img2_g=float(img2_g)/total2
img2_r=float(img2_r)/total2

ax1 = plt.subplot(1,2,1)
plt.xticks([0,1,2],["blue","green","red"],rotation=0)
plt.bar([0],[img1_b],1,color='b')
plt.bar([1],[img1_g],1,color='g')
plt.bar([2],[img1_r],1,color='r')
ax1.set_title("img1 color")

ax2 = plt.subplot(1,2,2)
plt.xticks([0,1,2],["blue","green","red"],rotation=0)
plt.bar([0],[img2_b],1,color='b')
plt.bar([1],[img2_g],1,color='g')
plt.bar([2],[img2_r],1,color='r')
ax2.set_title("img2 color")

plt.tight_layout()
plt.show()
