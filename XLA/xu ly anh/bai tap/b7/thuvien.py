import cv2
import numpy as np

# Đọc ảnh từ đường dẫn
img = cv2.imread("D:\\Ky 2 nam 3\\xu ly anh\\bai tap\\b7\\anh_hough.png")

# Chuyển ảnh màu sang ảnh xám
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Làm mờ ảnh bằng bộ lọc Gaussian
img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)

# Phát hiện biên bằng phương pháp Canny
edges = cv2.Canny(img_blur, 50, 150)

# Tạo mặt nạ ROI
mask = np.zeros_like(edges)
height, width = mask.shape
polygon = np.array([[(0, height), (width, height), (width, height//2), (0, height//2)]])
cv2.fillPoly(mask, polygon, 255)

# Áp dụng mặt nạ ROI
roi = cv2.bitwise_and(edges, mask)

# Biến đổi Hough Line
lines = cv2.HoughLinesP(roi, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)

# Vẽ các đường biên lên ảnh gốc
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Hiển thị ảnh
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
