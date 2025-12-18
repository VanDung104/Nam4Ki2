#Hashtag Nguyễn Đình Quý
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("D:\\Ky 2 nam 3\\xu ly anh\\bai tap\\b6\\btvn_NDQUY\\Bikesgray.jpg")
# Chuyển ảnh màu sang ảnh xám
R, G, B = img[:,:,2], img[:,:,1], img[:,:,0] # Tách kênh ảnh 
img_gray = 0.2989 * R + 0.5870 * G + 0.1140 * B 
plt.subplot(231)
plt.imshow(img[:,:,::-1])
plt.title("Đây là ảnh gốc")
plt.subplot(232)
plt.imshow(img_gray, cmap="gray")
plt.title("Đây là ảnh xám")

def Tich_chap(img, mask):
    h, w = img.shape
    m, n = mask.shape
    #mở rộng biên với các giá trị là 0
    # Ma trận 3 3 mở rộng là 5 5 
    pad_height = m // 2 #1
    pad_width = n // 2  #1
    img_pad = np.zeros((h + 2*pad_height, w + 2*pad_width), dtype=np.float64) # 5x5
    img_pad[pad_height:h+pad_height, pad_width:w+pad_width] = img # thêm viền vào ảnh

    img_out = np.zeros_like(img, dtype=np.float64)

    for i in range(pad_height, h + pad_height): #1, h+1
        for j in range(pad_width, w + pad_width): #1,w+1
            img_out[i-pad_height, j-pad_width] = np.sum(img_pad[i-pad_height:i+pad_height+1, j-pad_width:j+pad_width+1] * mask) # cắt viền và nhân và cộng. Quá trình tích chập 

    img_out = np.clip(img_out, 0, 255).astype(np.uint8)
    return img_out

# Phát hiện biên theo thuật toán Robert
# Kernel Robert theo X
RobertX = np.array([[0, 0, 0], [0, 1, 0], [0, 0, -1]])

# Kernel Robert theo Y
RobertY = np.array([[0, 0, 0], [0, 1, 0], [0, -1, 0]])

# Lọc Robert theo X
imgRobertX = Tich_chap(img_gray, RobertX)

# Lọc Robert theo Y
imgRobertY = Tich_chap(img_gray, RobertY)

# Ảnh tổng Robert theo X và Y
imgRobertXY = np.sqrt(np.power(imgRobertX.astype(np.float64), 2) + np.power(imgRobertY.astype(np.float64), 2))
plt.subplot(233)
plt.imshow(imgRobertXY, cmap="gray")
plt.title("Toán tử RobertXY")
# Phát hiện biên theo thuật toán Robert
# Kernel Robert theo X
RobertX = np.array([[0, 0, 0], [0, 1, 0], [0, 0, -1]])

# Kernel Robert theo Y
RobertY = np.array([[0, 0, 0], [0, 1, 0], [0, -1, 0]])

# Lọc Robert theo X
imgRobertX = Tich_chap(img_gray, RobertX)

# Lọc Robert theo Y
imgRobertY = Tich_chap(img_gray, RobertY)

# Ảnh tổng Robert theo X và Y
imgRobertXY = np.sqrt(np.power(imgRobertX, 2) + np.power(imgRobertY, 2))
plt.subplot(233)
plt.imshow(imgRobertXY, cmap="gray")
plt.title("Toán tử RobertXY")


#Phát hiện biên theo thuật toán SoBel
# Kernel Sobel theo hướng X
SobelX = np.array([[-1, 0, 1],[-2, 0, 2],[-1, 0, 1]])

# Kernel Sobel theo hướng Y
SobelY = np.array([[-1, -2, -1],[ 0,  0,  0],[ 1,  2,  1]])

# Lọc Sobel theo X 
imgSobelX = Tich_chap(img_gray, SobelX)

# Lọc Sobel theo Y 
imgSobelY = Tich_chap(img_gray, SobelY)

# Ảnh tổng Sobel theo  X và Y
imgSobelXY = np.sqrt(np.power(imgSobelX.astype(np.float64), 2) + np.power(imgSobelY.astype(np.float64), 2))
plt.subplot(234)
plt.imshow(imgSobelXY, cmap="gray")
plt.title("Toán tử SobelXY")

#Phát hiện biên theo thuật toán Prewitt
# Kernel Prewitt theo hướng X
PrewittX = np.array([[-1, 0, 1],[-1, 0, 1],[-1, 0, 1]])

# Kernel Prewitt theo hướng Y
PrewittY = np.array([[-1, -1, -1],[ 0,  0,  0],[ 1,  1,  1]])

# Lọc Prewitt theo X 
imgPrewittX = Tich_chap(img_gray, PrewittX)

# Lọc Prewitt theo Y 
imgPrewittY = Tich_chap(img_gray, PrewittY)

# Ảnh tổng Prewitt theo  X và Y
imgPrewittXY = np.sqrt(np.power(imgPrewittX.astype(np.float64), 2) + np.power(imgPrewittY.astype(np.float64), 2))
plt.subplot(235)
plt.imshow(imgPrewittXY, cmap="gray")
plt.title("Toán tử PrewittXY")

#Phát hiện biên theo thuật toán Laplace of Gaussian
# Kernel Laplace of Gaussian
LoG = np.array([[0, 0, -1, 0, 0],[0, -1, -2, -1, 0],[-1, -2, 16, -2, -1],[0, -1, -2, -1, 0], [0, 0, -1, 0, 0]])
                 
# Lọc Laplace of Gaussian
imgLoG = Tich_chap(img_gray, LoG)

plt.subplot(236)
plt.imshow(imgLoG, cmap="gray")
plt.title("Toán tử Laplace of Gauss")

plt.show()


