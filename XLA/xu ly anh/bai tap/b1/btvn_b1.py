#YcbCr_image = np.stack([Y,Cb,Cr]) hoặc np.clip
#YcbCr_image = np.stack([Y,Cb,Cr],axis=-) 
import cv2
import numpy as np
from matplotlib import pyplot as plt 

img = cv2.imread("D:\\Ky 2 nam 3\\xu ly anh\\bai tap\\b1\\lenna.webp")
print("Kich thuoc cua anh goc la: ", img.shape)
# Chuyển ảnh RGB sang ảnh xám 
R, G, B = img[:,:,2], img[:,:,1], img[:,:,0] # Tách kênh ảnh 
img_gray = 0.2989 * R + 0.5870 * G + 0.1140 * B

plt.subplot(321)
plt.imshow(img[:,:,::-1]) # Đảo ngược thứ tự lấy theo R G B với step = -1
plt.title("Đây là ảnh gốc")

plt.subplot(322)
plt.imshow(img_gray, cmap="gray") # Hiển thị ảnh xám 
plt.title("Đây là ảnh xám")

#Chuyển ảnh RGB sang ảnh 
# Tính toán Y, Cb, Cr
Y = np.uint8(16 + 219 * (0.299 * R + 0.587 * G + 0.114 * B) / 255.0)
Cb = np.uint8(128 + 224 * (-0.169 * R - 0.331 * G + 0.5 * B) / 255.0)
Cr = np.uint8(128 + 224 * (0.5 * R - 0.419 * G - 0.081 * B) / 255.0)

# Sử dụng np.array để tạo mảng chứa các kênh Y, Cr, Cb
ycbcr_image = np.array([Y, Cr, Cb])

plt.subplot(323)
plt.imshow(ycbcr_image.transpose(1, 2, 0))  # Định dạng lại vị trí cho thẳng cao rộng và độ sâu(kênh màu)
plt.title("Đây là ảnh YCbCr")
ycbcr_image1 = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
plt.subplot(324)
plt.imshow(ycbcr_image1) 
plt.title("Đây là ảnh YCbCr dùng thư viện")

#Chuyển hình ảnh RGB sang HSV 

R1= R/255.0
G1=G/255.0
B1=B/255.0
Cmax = np.maximum.reduce([R1, G1, B1])
Cmin = np.minimum.reduce([R1,G1, B1])
delta= Cmax-Cmin

H=np.zeros_like(Cmax) #ma trận H toàn 0 có kích thước ma trận của Cmax  

H[Cmax == R1] = 60 * ((G1[Cmax == R1] - B1[Cmax == R1]) / delta[Cmax == R1] % 6)  
H[Cmax == G1] = 60 * ((B1[Cmax == G1] - R1[Cmax == G1]) / delta[Cmax == G1] + 2) 
H[Cmax == B1] = 60 * ((R1[Cmax == B1] - G1[Cmax == B1]) / delta[Cmax == B1] + 4) 

S = np.where(Cmax == 0, 0, delta / Cmax) 
V = Cmax

# Hue nằm trong khoảng 0-360 
# Nếu H<0
H = (H + 360) % 360
#ép kiểu 
H = (H / 2).astype(np.uint8) # ảnh sử dụng 8 bit H <- H/2 để phù hợp với 0 đến 255
# S va V nam trong khoang [0,1]
S = (S * 255).astype(np.uint8)
V = (V * 255).astype(np.uint8)

Anh_HSV = cv2.merge([H, S, V]) # tron 3 ma tran lai theo thu tu HSV
plt.subplot(325)
plt.imshow(Anh_HSV)
plt.title("Ảnh HSV")
anh_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
plt.subplot(326)
plt.imshow(anh_hsv)
plt.title("Đây là ảnh HSV (dùng thư viện)")
plt.show()


