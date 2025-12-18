import numpy as np
#ham gauss
a = np.random.normal(2,1,6) #ky vong =2,lech chuan =1 , 6 phan tử 
print(a)
A = np.random.normal(2,1,[2,3]) # 2 hang 3 cot
print(A)
#Hàm poisson 
B = np.random.poisson([2,3])
print(B)
C = np.random.poisson(10)
print(C)
b= np.random.randint(0,10,8) #từ 0 - 9 và 8 phần tử
print(b)
c= np.random.randint(0,10,[2,3])
print(c)
d=np.random.randn(8) # nguy = 0(giá trị kỳ vọng) xích ma(phương sai) =1 , chuẩn tắt
print(d)
#Chuyển 1 ảnh màu sang ảnh xám 
#sinh ra 3 anh nhieu nhieu gauss nhieu salt peper  possion
#1 anh nhieu 2 anh loc . Loc trung bình va lọc trung vị
#Về làm sau khi lọc trung bình mà vẫn giữ nguyên kích thước ảnh ban đầu