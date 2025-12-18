import numpy as np
import cv2
import matplotlib.pyplot as plt

def Loc_Trung_binh_hinh_hoc(img, ksize):
    m, n = img.shape
    img_ket_qua_anh_loc = np.zeros([m, n])
    h=(ksize -1) // 2
    padded_img = np.pad(img, (h, h), mode='reflect')
    for i in range(m):
        for j in range(n):
            vung_anh_kich_thuoc_k = padded_img[i:i+ksize,j:j+ksize]
            gia_tri_TB_cuc_bo = np.mean(vung_anh_kich_thuoc_k)
            gia_tri_loc = np.prod(vung_anh_kich_thuoc_k) ** (1.0 / m * n)
            if gia_tri_loc > gia_tri_TB_cuc_bo:
               img_ket_qua_anh_loc[i, j]= int(gia_tri_TB_cuc_bo)
            else:
               img_ket_qua_anh_loc[i,j] = int(gia_tri_loc)
    return img_ket_qua_anh_loc

if __name__ == "__main__":
    img_nhieu = cv2.imread('Anh_nhieu_de_loc_Trung_binh.tif', 0)
    ksize =3
    img_ket_qua_TBHH = Loc_Trung_binh_hinh_hoc(img_nhieu, ksize)

    fig = plt.figure(figsize=(16, 9))     # Thiết lập vùng (cửa sổ) vẽ
    ax1, ax2 = fig.subplots(1, 2)        # Thiết lập 2 vùng con ax1, ax2
    ax1.imshow(img_nhieu, cmap='gray')      # Hiển thị ảnh gốc vùng ax1
    ax1.set_title("ảnh gốc bị nhiễu Gaussian") # Thiết lập tiêu đề vùng ax1
    ax1.axis("off")

    ax2.imshow(img_ket_qua_TBHH, cmap='gray')  # Hiển thị ảnh sau khi lọc
    ax2.set_title("ảnh sau khi lọc Trung bình hình học")  # Thiết lập tiêu đề vùng ax2
    ax2.axis("off")

    plt.show()