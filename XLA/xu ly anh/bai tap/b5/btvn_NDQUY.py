import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("D:\\Ky 2 nam 3\\xu ly anh\\bai tap\\b5\\9452d24b-62e3-40dd-91e4-2606e9fc759f.jpg")

R, G, B = img[:, :, 2], img[:, :, 1], img[:, :, 0]
img_gray = 0.2989 * R + 0.5870 * G + 0.1140 * B  # Công thức chuyển đổi sang ảnh xám
img_gray = img_gray.astype(np.uint8)

def fft(image):
    F = np.fft.fft2(image)
    Fshift = np.fft.fftshift(F)
    return F, Fshift

def ifft(Fshift, H):
    Gshift = Fshift * H
    G = np.fft.ifftshift(Gshift)
    return G

def butterworth_lowpass_function(image, D0, n):
    M, N = image.shape

    # Tính toán phổ Fourier của ảnh
    F, Fshift = fft(image)

    # Tạo ma trận bộ lọc Butterworth low-pass
    H = np.zeros((M, N), dtype=np.float32)
    for u in range(M):
        for v in range(N):
            D = np.sqrt((u - M/2)**2 + (v - N/2)**2)
            H[u, v] = 1 / (1 + (D/D0)**(2*n))

    # Áp dụng bộ lọc vào không gian tần số
    G = ifft(Fshift, H)

    # Tính toán ảnh lọc trong không gian thời gian
    g = np.abs(np.fft.ifft2(G))
    return g

def gaussian_lowpass_function(image, sigma):
    M, N = image.shape

    # Tính toán phổ Fourier của ảnh
    F, Fshift = fft(image)

    # Tạo ma trận bộ lọc Gauss low-pass
    H = np.zeros((M, N), dtype=np.float32)
    for u in range(M):
        for v in range(N):
            D = np.sqrt((u - M/2)**2 + (v - N/2)**2)
            H[u, v] = np.exp(-D**2 / (2*sigma**2))

    # Áp dụng bộ lọc vào không gian tần số
    G = ifft(Fshift, H)

    # Tính toán ảnh lọc trong không gian thời gian
    g = np.abs(np.fft.ifft2(G))
    return g

# Áp dụng bộ lọc thông thấp Butterworth và Gaussian
D0_butterworth = 15  # Tần số cắt của bộ lọc Butterworth
n_butterworth = 2  # Bậc của bộ lọc Butterworth
filtered_image_butterworth = butterworth_lowpass_function(img_gray, D0_butterworth, n_butterworth)

sigma_gaussian = 10  # Độ lớn của bộ lọc Gaussian
filtered_image_gaussian = gaussian_lowpass_function(img_gray, sigma_gaussian)

# Hiển thị ảnh gốc và ảnh sau khi lọc
plt.subplot(131)
plt.imshow(img_gray, cmap='gray')
plt.title("Ảnh gốc")

plt.subplot(132)
plt.imshow(filtered_image_butterworth, cmap='gray')
plt.title("Butterworth LP")

plt.subplot(133)
plt.imshow(filtered_image_gaussian, cmap='gray')
plt.title("Gaussian LP")

plt.show()
