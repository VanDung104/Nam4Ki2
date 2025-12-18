import numpy as np
from matplotlib import pyplot as plt

# Đọc ảnh từ đường dẫn
img = plt.imread("D:\\Ky 2 nam 3\\xu ly anh\\bai tap\\b7\\lane.png")

# Chuyển ảnh màu sang ảnh xám
img_gray = np.dot(img[...,:3], [0.2989, 0.5870, 0.1140])

# Hiển thị ảnh gốc
plt.subplot(231)
plt.imshow(img)
plt.title("Ảnh gốc")

# Định nghĩa hàm tích chập
def convolution(image, kernel):
    h, w = image.shape
    m, n = kernel.shape
    pad_height = m // 2
    pad_width = n // 2
    img_pad = np.zeros((h + 2 * pad_height, w + 2 * pad_width))
    img_pad[pad_height:h + pad_height, pad_width:w + pad_width] = image
    img_out = np.zeros_like(image)

    for i in range(pad_height, h + pad_height):
        for j in range(pad_width, w + pad_width):
            img_out[i - pad_height, j - pad_width] = np.sum(img_pad[i - pad_height:i + pad_height + 1,
                                                   j - pad_width:j + pad_width + 1] * kernel)

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

    Ix = convolution(img, SobelX)
    Iy = convolution(img, SobelY)

    G = np.sqrt(np.power(Ix, 2) + np.power(Iy, 2))
    G = G / G.max() * 255
    theta = np.arctan2(Iy, Ix)
    return (G, theta)

# Định nghĩa hàm giảm cực đại
def non_max_suppression(img, D):
    M, N = img.shape
    Z = np.zeros((M, N), dtype=np.int64)
    angle = D * 180. / np.pi
    angle[angle < 0] += 180

    for i in range(1, M - 1):
        for j in range(1, N - 1):
            try:
                q = 255
                r = 255

                if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                    q = img[i, j + 1]
                    r = img[i, j - 1]
                elif (22.5 <= angle[i, j] < 67.5):
                    q = img[i + 1, j - 1]
                    r = img[i - 1, j + 1]
                elif (67.5 <= angle[i, j] < 112.5):
                    q = img[i + 1, j]
                    r = img[i - 1, j]
                elif (112.5 <= angle[i, j] < 157.5):
                    q = img[i - 1, j - 1]
                    r = img[i + 1, j + 1]

                if (img[i, j] >= q) and (img[i, j] >= r):
                    Z[i, j] = img[i, j]
                else:
                    Z[i, j] = 0
            except IndexError as e:
                pass

    return Z

# Định nghĩa hàm ngưỡng
def threshold(img, lowThresholdRatio=0.05, highThresholdRatio=0.09):
    highThreshold = img.max() * highThresholdRatio
    lowThreshold = highThreshold * lowThresholdRatio

    M, N = img.shape
    res = np.zeros((M, N), dtype=np.int64)

    strong = np.int64(255)
    weak = np.int64(25)

    strong_i, strong_j = np.where(img >= highThreshold)
    zeros_i, zeros_j = np.where(img < lowThreshold)
    weak_i, weak_j = np.where((img <= highThreshold) & (img >= lowThreshold))

    res[strong_i, strong_j] = strong
    res[weak_i, weak_j] = weak

    return (res, weak, strong)

# Định nghĩa hàm kết hợp các điểm yếu và mạnh
def hysteresis(img, weak, strong=255):
    M, N = img.shape
    for i in range(1, M - 1):
        for j in range(1, N - 1):
            if (img[i, j] == weak):
                try:
                    if ((img[i + 1, j - 1] == strong) or (img[i + 1, j] == strong) or (img[i + 1, j + 1] == strong)
                        or (img[i, j - 1] == strong) or (img[i, j + 1] == strong)
                        or (img[i - 1, j - 1] == strong) or (img[i - 1, j] == strong) or (img[i - 1, j + 1] == strong)):
                        img[i, j] = strong
                    else:
                        img[i, j] = 0
                except IndexError as e:
                    pass

    return img

# Định nghĩa hàm phát hiện biên Canny
def canny_edge_detection(img, sigma=1, kernel_size=5, lowThreshold=0.05, highThreshold=0.15):
    img_smoothed = convolution(img_gray, gaussian_kernel(kernel_size, sigma))
    gradientMat, thetaMat = sobel_filters(img_smoothed)
    nonMaxImg = non_max_suppression(gradientMat, thetaMat)
    thresholdImg , weak , strong = threshold(nonMaxImg, lowThreshold, highThreshold)
    img_final = hysteresis(thresholdImg,weak,strong)
    return img_final

final_img = canny_edge_detection(img)

# Hiển thị ảnh phát hiện biên Canny
plt.subplot(232)
plt.imshow(final_img, cmap="gray")
plt.title("Ảnh phát hiện biên Canny")

def hough_line(img):
    thetas = np.deg2rad(np.arange(-90.0, 90.0))
    width, height = img.shape
    diag_len = np.ceil(np.sqrt(width * width + height * height))
    rhos = np.linspace(-diag_len, diag_len, int(diag_len * 2.0))

    cos_t = np.cos(thetas)
    sin_t = np.sin(thetas)
    num_thetas = len(thetas)

    accumulator = np.zeros((int(2 * diag_len), num_thetas), dtype=np.uint64)  # kích thước của ảnh
    y_idxs, x_idxs = np.nonzero(img)

    for i in range(len(x_idxs)):
        x = x_idxs[i]
        y = y_idxs[i]
        for t_idx in range(num_thetas):
            rho = round(x * cos_t[t_idx] + y * sin_t[t_idx]) + int(diag_len)
            accumulator[rho, t_idx] += 1
    return accumulator, thetas, rhos

accumulator, thetas, rhos = hough_line(final_img)
plt.subplot(233)
plt.plot(thetas, accumulator.sum(axis=0))
plt.title("Mặt phẳng Hough Hough cho 1 điểm")
plt.xlabel("Góc (rad)")
plt.ylabel("Rho")
plt.axis('image')
# Hiển thị không gian Hough cho 2 điểm
plt.subplot(234)
plt.imshow(accumulator, cmap='gray', extent=[np.rad2deg(thetas[-1]), np.rad2deg(thetas[0]), rhos[-1], rhos[0]])
plt.title("Mặt phẳng Hough cho 2 điểm")
plt.xlabel("Góc (độ)")
plt.ylabel("Rho")
plt.axis('image')

plt.tight_layout()
# Hiển thị không gian Hough
plt.subplot(235)
plt.imshow(np.log(accumulator + 1), cmap='gray', extent=[np.rad2deg(thetas[-1]), np.rad2deg(thetas[0]), rhos[-1], rhos[0]])
plt.title("Mặt phẳng Hough")
plt.xlabel("Góc (độ)")
plt.ylabel("Rho")
plt.axis('image')
plt.show()
