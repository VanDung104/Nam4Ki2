import cv2
from matplotlib import pyplot as plt
import numpy as np

# Đọc ảnh từ đường dẫn
img = cv2.imread("D:\\Ky 2 nam 3\\xu ly anh\\bai tap\\b7\\lane.png")

# Chuyển ảnh màu sang ảnh xám
R, G, B = img[:,:,2], img[:,:,1], img[:,:,0] # Tách kênh ảnh 
img_gray = 0.2989 * R + 0.5870 * G + 0.1140 * B 

# Hiển thị ảnh gốc
plt.subplot(131)
plt.imshow(img[:,:,::-1])
plt.title("Đây là ảnh gốc")

# Hiển thị ảnh xám
plt.subplot(132)
plt.imshow(img_gray, cmap="gray")
plt.title("Đây là ảnh xám")

# Định nghĩa hàm tích chập
def Tich_chap(img, mask):
    h, w = img.shape
    m, n = mask.shape
    #Kernel thường là ma trận vuông
    pad_height = m // 2 #1
    pad_width = n // 2 #1
     #mở rộng biên với các giá trị là 0
    # Ma trận 3 3 mở rộng là 5 5 
    img_pad = np.zeros((h + 2*pad_height, w + 2*pad_width), dtype=np.float64) # 5x5
    img_pad[pad_height:h+pad_height, pad_width:w+pad_width] = img  # thêm viền vào ảnh

    img_out = np.zeros_like(img, dtype=np.float64)
    #Code cũ 
    # for i in range(pad_height, h + pad_height):
    #     for j in range(pad_width, w + pad_width):
    #         img_out[i-pad_height, j-pad_width] = np.sum(img_pad[i-pad_height:i+pad_height+1, j-pad_width:j+pad_width+1] * mask) # cắt viền và nhân và cộng. Quá trình tích chập 
    #         #img_out[i,j] = np.sum(img_pad[m])
    # img_out = np.clip(img_out, 0, 255).astype(np.uint8)
    # return img_out

    #Sau khi sửa 
    for i in range(0, h ):
        for j in range(0, w ):
            img_out[i, j] = np.sum(img_pad[i:i+m, j:j+n] * mask) # cắt viền và nhân và cộng. Quá trình tích chập 
    img_out = np.clip(img_out, 0, 255).astype(np.uint8)
    return img_out

# Định nghĩa hàm kernel Gaussian
def gaussian_kernel(size, sigma=1):
    size = int(size) // 2
    x, y = np.mgrid[-size:size+1, -size:size+1]
    normal = 1 / (2.0 * np.pi * sigma**2)
    g =  np.exp(-((x**2 + y**2) / (2.0*sigma**2))) * normal
    return g

# Định nghĩa hàm lọc Sobel
def sobel_filters(img):
    SobelX = np.array([[-1, 0, 1],[-2, 0, 2],[-1, 0, 1]])
    SobelY = np.array([[-1, -2, -1],[ 0,  0,  0],[ 1,  2,  1]])

    Ix = Tich_chap(img, SobelX)
    Iy = Tich_chap(img, SobelY)

    G = np.sqrt(np.power(Ix.astype(np.float64), 2) + np.power(Iy.astype(np.float64), 2))
    G = G / G.max() * 255
    theta = np.arctan2(Iy, Ix) 
    return (G, theta)

# Định nghĩa hàm giảm cực đại
def non_max_suppression(img, D):
    M, N = img.shape
    Z = np.zeros((M,N), dtype=np.int64)
    #Nếu góc alpha <0 + thêm pi
    angle = D

    for i in range(1,M-1):
        for j in range(1,N-1):
            try:
                q = 255
                r = 255

                if (0 <= angle[i,j] < np.pi/8) or (7*np.pi/8 <= angle[i,j] <= np.pi):
                    q = img[i, j+1] #Các điểm lân cận
                    r = img[i, j-1]
                elif (np.pi/8 <= angle[i,j] < 3*np.pi/8):
                    q = img[i+1, j-1]
                    r = img[i-1, j+1]
                elif (3*np.pi/8 <= angle[i,j] < 5*np.pi/8):
                    q = img[i+1, j]
                    r = img[i-1, j]
                elif (5*np.pi/8 <= angle[i,j] < 7*np.pi/8):
                    q = img[i-1, j-1]
                    r = img[i+1, j+1]

                if (img[i,j] >= q) and (img[i,j] >= r):
                    Z[i,j] = img[i,j] # Lớn hơn các điểm lân cận thì là cực đại
                else:
                    Z[i,j] = 0
            except IndexError as e:
                pass

    return Z

# Định nghĩa hàm ngưỡng
def threshold(img, lowThresholdRatio=0.05, highThresholdRatio=0.09):
    highThreshold = img.max() * highThresholdRatio
    lowThreshold = highThreshold * lowThresholdRatio

    M, N = img.shape
    res = np.zeros((M,N), dtype=np.int64)

    strong = np.int64(255)
    weak = np.int64(25)

    strong_i, strong_j = np.where(img >= highThreshold)
    zeros_i, zeros_j = np.where(img < lowThreshold) # nhỏ hơn ngưỡng thấp thì bằng 0

    weak_i, weak_j = np.where((img <= highThreshold) & (img >= lowThreshold)) #nằm trong ngưỡng thấp và ngưỡng cao

    res[strong_i, strong_j] = strong
    res[weak_i, weak_j] = weak

    return (res , weak , strong)

# Định nghĩa hàm kết hợp các điểm yếu và mạnh
def hysteresis(img, weak, strong=255):
    M, N = img.shape
    for i in range(1, M-1):
        for j in range(1, N-1):
            if (img[i,j] == weak):
                try:
                    if ((img[i+1, j-1] == strong) or (img[i+1, j] == strong) or (img[i+1, j+1] == strong)
                        or (img[i, j-1] == strong) or (img[i, j+1] == strong)
                        or (img[i-1, j-1] == strong) or (img[i-1, j] == strong) or (img[i-1, j+1] == strong)):
                        img[i, j] = strong
                    else:
                        img[i, j] = 0
                except IndexError as e: # có lỗi thì bỏ         
                    pass

    return img

# Định nghĩa hàm phát hiện biên Canny
def canny_edge_detection(img, sigma=1, kernel_size=5, lowThreshold=0.05, highThreshold=0.15):
    img_smoothed = Tich_chap(img_gray, gaussian_kernel(kernel_size, sigma))
    gradientMat, thetaMat = sobel_filters(img_smoothed)
    nonMaxImg = non_max_suppression(gradientMat, thetaMat)
    thresholdImg , weak , strong = threshold(nonMaxImg, lowThreshold, highThreshold)
    img_final = hysteresis(thresholdImg,weak,strong)
    return img_final


final_img = canny_edge_detection(img)

# Hiển thị ảnh phát hiện biên Canny
plt.subplot(133)
plt.imshow(final_img, cmap="gray")
plt.title("Ảnh phát hiện biên Canny")
plt.show()

















































#NDQUY























