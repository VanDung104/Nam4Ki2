import cv2
import numpy as np
from matplotlib import pyplot as plt 

img = cv2.imread("D:\\Ky 2 nam 3\\xu ly anh\\bai tap\\b1\\lenna.webp")

# Chuyển ảnh RGB sang ảnh xám 
R, G, B = img[:,:,2], img[:,:,1], img[:,:,0] # Tách kênh ảnh 
img_gray = 0.2989 * R + 0.5870 * G + 0.1140 * B

plt.subplot(221)
plt.imshow(img[:,:,::-1]) # Đảo ngược thứ tự lấy theo R G B với step = -1
plt.title("Đây là ảnh gốc")

plt.subplot(222)
plt.imshow(img_gray, cmap="gray") # Hiển thị ảnh xám 
plt.title("Đây là ảnh xám")

#Chuyển ảnh RGB sang ảnh YCbCr

ycbcr_image = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
plt.subplot(223)
plt.imshow(ycbcr_image) 
plt.title("Đây là ảnh YCbCr ")

#Chuyển hình ảnh RGB sang HSV 

img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
plt.subplot(224)
plt.imshow(img_hsv)
plt.title("Đây là ảnh HSV ")
plt.show()


