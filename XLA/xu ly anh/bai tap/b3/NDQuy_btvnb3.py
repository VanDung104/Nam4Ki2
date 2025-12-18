import cv2
import random
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("D:\\Downloadload\\gray.webp")

# Chuyển ảnh màu sang ảnh xám
R, G, B = img[:,:,2], img[:,:,1], img[:,:,0] # Tách kênh ảnh 
img_gray = 0.2989 * R + 0.5870 * G + 0.1140 * B

plt.subplot(251)
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
plt.subplot(252)
plt.imshow(cv2.cvtColor(Ig,cv2.COLOR_BGR2RGB))
plt.title("Nhiễu Gauss")

# Salt & Pepper Noise
def sp_noise(image, prob): #xác suất nhiễu màu đen 
    output = np.zeros(img.shape, np.uint8)
    thres = 1 - prob # xác suất nhiễu màu trắng 
    for i in range(img.shape[0]): #hàng
        for j in range(img.shape[1]): #cột
            for k in range(img.shape[2]): #kênh màu
                rdn = random.random()
                if rdn < prob:
                    output[i][j][k] = 0
                elif rdn > thres:
                    output[i][j][k] = 255
                else:
                    output[i][j][k] = image[i][j][k]
    return output

 
sp_img = sp_noise(img,0.05)
plt.subplot(253)
plt.imshow(cv2.cvtColor(sp_img, cv2.COLOR_BGR2RGB)) 
plt.title("Salt & pepper noise")
# Poisson Noise
def poisson_noise(image):
    noisy_img = np.zeros_like(image)
    for i in range(image.shape[0]): #hàng
        for j in range(image.shape[1]): #cột
            for k in range(image.shape[2]): # 3 channels 
                value = image[i][j][k]
                noisy_value = np.random.poisson(value)
                noisy_img[i][j][k] = np.clip(noisy_value, 0, 255).astype(np.uint8)
    return noisy_img

poisson_img = poisson_noise(img)
plt.subplot(254)
plt.imshow(cv2.cvtColor(poisson_img, cv2.COLOR_BGR2RGB))
plt.title("Nhiễu Poisson")

def Tich_chap(img, mask):
    h, w = img_gray.shape
    img_new = np.zeros((h-2, w-2))  # Ảnh mới sẽ nhỏ hơn ảnh gốc
    for i in range(1, h-1):
        for j in range(1, w-1):
            img_new[i-1, j-1] = np.sum(img_gray[i-1:i+2, j-1:j+2] * mask)
    img_new = np.clip(img_new, 0, 255).astype(np.uint8)
    return img_new


# Tạo ma trận mask cho bộ lọc trung bình
LOC_TB = np.ones((3, 3), dtype=np.float32) / 9

# Áp dụng tích chập với mask đã tạo lên ảnh có nhiễu Gauss
filtered_gauss = Tich_chap(Ig, LOC_TB)
filtered_sp = Tich_chap(sp_img, LOC_TB)
filtered_poisson = Tich_chap(poisson_img, LOC_TB)

plt.subplot(255)
plt.imshow(filtered_gauss, cmap='gray')
plt.title("Lọc TB của Gauss")

plt.subplot(256)
plt.imshow(filtered_sp, cmap='gray')
plt.title("Lọc TB của SP")

plt.subplot(257)
plt.imshow(filtered_poisson, cmap='gray')
plt.title("Lọc TB của poisson")
def loc_trung_vi(Img):
    m,n = img_gray.shape
    img_new = np.zeros((m-2,n-2), dtype=np.uint8) #cắt biên
    for i in range (1,m-1):
        for j in range (1,n-1):
            temp = img_gray[i-1:i+2,j-1:j+2]
            temp = np.sort(temp.flatten()) #làm phẳng ma trận thành mảng
            img_new[i-1,j-1] = temp[4] #vị trí trung vị 
    return img_new
trungvi_gauss = loc_trung_vi(Ig)
trungvi_sp = loc_trung_vi(sp_img)
trungvi_poisson = loc_trung_vi(poisson_img)
plt.subplot(258)
plt.imshow(trungvi_gauss,cmap='gray')
plt.title("Lọc trung vị gauss")
plt.subplot(259)
plt.imshow(trungvi_sp,cmap='gray')
plt.title("Lọc trung vị sp")
plt.subplot(2,5,10)
plt.imshow(trungvi_poisson,cmap='gray')
plt.title("Lọc trung vị poisson")
plt.show()