import numpy as np
import matplotlib.pyplot as plt
import cv2

# Tạo một hình ảnh màu đen với một điểm màu trắng
image = np.zeros((100, 100), dtype=np.uint8)
x, y = 50, 50
image[x, y] = 255

# Hiển thị hình ảnh
plt.figure(figsize=(5, 5))
plt.imshow(image, cmap='gray')
plt.title('Hình ảnh gốc')
plt.show()

# Thực hiện biến đổi Hough
edges = cv2.Canny(image, 50, 150, apertureSize=3)
lines = cv2.HoughLines(edges, 1, np.pi/180, 15)

# Biểu diễn các đường thẳng tìm được trong không gian hình ảnh
image_with_lines = np.copy(image)
for rho, theta in lines[:, 0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    cv2.line(image_with_lines, (x1, y1), (x2, y2), (255, 0, 0), 1)

# Hiển thị hình ảnh với các đường thẳng
plt.figure(figsize=(5, 5))
plt.imshow(image_with_lines, cmap='gray')
plt.title('Hình ảnh với các đường thẳng')
plt.show()
