import numpy as np
a = np.array([[1,2,3],[4,5,6],[7,8,9]])
print(a)
print(a.shape)
b = np.array([[0,1,0],[1,-4,1],[0,1,0]])
print(b)
c=a*b # =b*a
print(c)
d = np.dot(a,b) #Phép nhân ma trận A.B # B.A
print(d)
print(c.sum()) #tổng của ma trận
print(c.sum())
#lọc sắc nét & lọc high boost
#dùng hàm tích chập
#đọc ảnh RGB -> gray
#tạo nhiễu
#cộng nhiễu vào ảnh
#lọc nhiễu sử dụng bộ lọc sắc nét và high boost
