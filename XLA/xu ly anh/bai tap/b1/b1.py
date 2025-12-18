import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("D:\\Downloadload\\anh-meo-den-dep-14-05-23-00-01.jpg")
print("Kich thuoc cua anh goc la: ", img.shape)
R, G, B = img[:,:,2], img[:,:,1], img[:,:,0]
img_gray = 0.2989 * R + 0.5870 * G + 0.1140 * B #CONG THUC ANH XAM TRONG TEAMS
# img_gray1 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
img_amban=L-1-img_gray
plt.subplot(221)
plt.imshow(img[:,:,::-1])
plt.title("day la anh goc")

plt.subplot(222)
plt.imshow(img_gray, cmap = "gray")
plt.title("anh muc xam")

plt.subplot(223)
plt.imshow(img_amban, cmap = "gray")
plt.title("anh am ban")

plt.subplot(224)
plt.imshow(img_hsv)
plt.title("anh hsv")

plt.show()