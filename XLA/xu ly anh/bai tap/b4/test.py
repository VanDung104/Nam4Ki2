import cv2
import random
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("D:\\Downloadload\\gray.webp")

# Chuyển ảnh màu sang ảnh xám
R, G, B = img[:,:,2], img[:,:,1], img[:,:,0] # Tách kênh ảnh 
img_gray = 0.2989 * R + 0.5870 * G + 0.1140 * B

plt.subplot(221)
plt.imshow(img[:,:,::-1]) # Đảo ngược thứ tự lấy theo R G B với step = -1
plt.title("Đây là ảnh gốc")

# Gauss Noise 
mean = 0 # gia tri trung binh
variance = 2000  # Phương sai 
row, col, ch = img.shape
sigma = variance**0.5 # độ lệch chuẩn (căn bậc 2 của phương sai)
gauss = np.random.normal(mean, sigma, (row, col, ch))  
Ig = img + gauss # Cộng 1 gia tri nhieu ngau nhien vao 
Ig = np.clip(Ig, 0, 255).astype(np.uint8)
plt.subplot(222)
plt.imshow(cv2.cvtColor(Ig,cv2.COLOR_BGR2RGB))
plt.title("Nhiễu Gauss")

#Giữ nguyên ảnh
# def Tich_chap(img, mask):
#     h, w = img_gray.shape
#     img_new = np.zeros_like(img_gray)
#     img_padded = np.pad(img_gray, pad_width=1, mode='edge')  # Mở rộng ảnh
#     for i in range(1, h+1):
#         for j in range(1, w+1):
#             img_new[i-1, j-1] = np.sum(img_padded[i-1:i+2, j-1:j+2] * mask)
#     img_new = np.clip(img_new, 0, 255).astype(np.uint8)
#     return img_new

# def Tich_chap(img, mask):
#     h, w = img_gray.shape
#     img_new = np.zeros((h-2, w-2))  # Ảnh mới sẽ nhỏ hơn ảnh gốc
#     for i in range(1, h-1):
#         for j in range(1, w-1):
#             img_new[i-1, j-1] = np.sum(img_gray[i-1:i+2, j-1:j+2] * mask)
#     img_new = np.clip(img_new, 0, 255).astype(np.uint8)
#     return img_new


# # Tạo ma trận mask cho bộ lọc trung bình
# LOC_TB = np.ones((3, 3), dtype=np.float32) / 25

# # Áp dụng tích chập với mask đã tạo lên ảnh có nhiễu Gauss
# filtered_gauss = Tich_chap(Ig, LOC_TB)

# plt.subplot(133)
# plt.imshow(filtered_gauss, cmap='gray')
# plt.title("Lọc TB của Gauss")
def loc_trung_vi(img):
    m,n = img_gray.shape
    img_new = np.zeros((m-2,n-2), dtype=np.uint8) #cắt biên
    for i in range (1,m-1):
        for j in range (1,n-1):
            temp = img_gray[i-1:i+2,j-1:j+2]
            temp = np.sort(temp.flatten()) #làm phẳng ma trận thành mảng
            img_new[i-1,j-1] = temp[4] #vị trí trung vị 
    return img_new

trungvi_img = loc_trung_vi(Ig)
gauss_median = cv2.medianBlur(Ig, 3)
plt.subplot(223)
plt.imshow(trungvi_img,cmap='gray')
plt.title("Lọc trung vị gauss")

plt.subplot(224)
plt.imshow(cv2.cvtColor(gauss_median, cv2.COLOR_BGR2GRAY), cmap='gray')
plt.title("Lọc trung vị thư viện")
plt.show()
