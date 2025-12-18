import cv2
import random
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("D:\\Downloadload\\gray.webp")

# Chuyển ảnh màu sang ảnh xám
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
plt.subplot(251)
plt.imshow(img)
plt.title("Ảnh gốc")

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

# Lọc trung bình
gauss_blur = cv2.blur(Ig, (5,5))
sp_blur = cv2.blur(sp_img, (5,5))
poisson_blur = cv2.blur(poisson_img, (5,5))
plt.subplot(255)
plt.imshow(cv2.cvtColor(gauss_blur, cv2.COLOR_BGR2GRAY), cmap='gray')
plt.title('Lọc TB của Gauss')

plt.subplot(256)
plt.imshow(cv2.cvtColor(sp_blur, cv2.COLOR_BGR2GRAY), cmap='gray')
plt.title('Lọc TB của S&P')

plt.subplot(257)
plt.imshow(cv2.cvtColor(poisson_blur, cv2.COLOR_BGR2GRAY), cmap='gray')
plt.title('Lọc TB của Poisson')

# Lọc trung vị
gauss_median = cv2.medianBlur(Ig, 5)
sp_median = cv2.medianBlur(sp_img, 5)
poisson_median = cv2.medianBlur(poisson_img, 5)
plt.subplot(258)
plt.imshow(cv2.cvtColor(gauss_median, cv2.COLOR_BGR2GRAY), cmap='gray')
plt.title('Lọc Trung vị của Gauss')

plt.subplot(259)
plt.imshow(cv2.cvtColor(sp_median, cv2.COLOR_BGR2GRAY), cmap='gray')
plt.title('Lọc Trung vị của S&P')

plt.subplot(2,5,10)
plt.imshow(cv2.cvtColor(poisson_median, cv2.COLOR_BGR2GRAY), cmap='gray')
plt.title('Lọc Trung vị của Poisson')

plt.show()
