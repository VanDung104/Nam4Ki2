import numpy as np
import cv2
import matplotlib.pyplot as plt


def Loc_Trung_Vi_thich_nghi(img,ksize,Smax):     # Định nghĩa hàm lọc trung vị thích nghi
    m,n = img.shape  # lấy 2 chiều của ảnh
    img_ket_qua_anh_loc= np.zeros([m, n]) # Tạo ma trận có kích thước bằng kích thước mxn
                                          # để lưu ảnh kết quả lọc
    h = (Smax-1)//2    # Thêm số pixel vào lề ảnh. Chú ý nếu bộ lọc có kích thước K thì:
                       # số pixel thêm vào mỗi lề ảnh (chú ý: ảnh có 4 lề) là (K-1)/2
    padded_img = np.pad(img,(h,h),mode='reflect')  #Thêm lề ảnh
    for i in range(m):
        for j in range(n):
            k = ksize
            vung_anh_kich_thuoc_k = padded_img[i:i+k,j:j+k] # tạo vùng lân cận (i,j)
                                                                     # Và cũng chính là vùng Sxy
            while True:
                # Bước A
                A1 = np.median(vung_anh_kich_thuoc_k) - np.min(vung_anh_kich_thuoc_k)
                A2 = np.median(vung_anh_kich_thuoc_k) - np.max(vung_anh_kich_thuoc_k)
                if A1 > 0 and A2 <0:
                    # Đi đến Bước B
                    # Chú ý: Giữ liệu các pixel số nguyên trong vùng [0..255]
                    # Nếu không chuyển sang int khi trừ thì chương trình sẽ cảnh báo
                    B1 = int(img[i, j]) - int(np.min(vung_anh_kich_thuoc_k))
                    B2 = int(img[i, j]) - int(np.max(vung_anh_kich_thuoc_k))
                    if B1>0 and B2 <0:
                        img_ket_qua_anh_loc[i,j] = img[i,j]
                    else:
                        img_ket_qua_anh_loc[i, j] = np.median(vung_anh_kich_thuoc_k)
                    break  # Thoát khỏi lặp
                else: # Quay lại bước A
                    k += 1
                    Snew = k*2+1
                    if Snew <= Smax :
                        vung_anh_kich_thuoc_k = padded_img[i:i+k,j:j+k]
                    else :
                        img_ket_qua_anh_loc[i,j] = np.median(vung_anh_kich_thuoc_k)
                        break # Thoát khỏi lặp
    return img_ket_qua_anh_loc

if __name__ == "__main__":
    img_nhieu = cv2.imread('Anh_nhieu_de_loc_trung_vi_thich_nghi.tif',0) # Đọc ảnh
    ksize=7   # Kích thước khởi tạo của bộ lọc thường là số lẽ
    Smax=11    # Kích thước tối đa của bộ lọc
    img_ket_qua = Loc_Trung_Vi_thich_nghi(img_nhieu,ksize, Smax)    #Gọi hàm lọc trung vị

    fig = plt.figure(figsize=(16, 9))     # Thiết lập vùng (cửa sổ) vẽ
    ax1, ax2 = fig.subplots(1, 2)        # Thiết lập 2 vùng con ax1, ax2
    ax1.imshow(img_nhieu, cmap='gray')      # Hiển thị ảnh gốc vùng ax1
    ax1.set_title("ảnh nhiễu muối tiêu")    # Thiết lập tiêu đề vùng ax1
    ax1.axis("off")

    ax2.imshow(img_ket_qua, cmap='gray') # Hiển thị ảnh sau khi lọc
    ax2.set_title("ảnh sau khi qua Bộ lọc trung vị thích nghi") # Thiết lập tiêu đề vùng ax2
    ax2.axis("off")

    plt.show()
