import numpy as np
import cv2
import matplotlib.pyplot as plt

def Loc_Thich_Nghi_Cuc_Bo(img, ksize, phuong_sai_nhieu):
    m, n = img.shape
    img_ket_qua_anh_loc = np.zeros([m, n])
    h=(ksize -1) // 2
    padded_img = np.pad(img, (h, h), mode='reflect')
    for i in range(m):
        for j in range(n):
            vung_anh_kich_thuoc_k = padded_img[i:i+ksize,j:j+ksize]
            phuong_sai_cuc_bo = np.var(vung_anh_kich_thuoc_k)
            gia_tri_TB_cuc_bo = np.mean(vung_anh_kich_thuoc_k)
            if gia_tri_TB_cuc_bo  > phuong_sai_nhieu :
                img_ket_qua_anh_loc[i,j] = gia_tri_TB_cuc_bo
            else:
                img_ket_qua_anh_loc[i,j] = padded_img[i,j] - int((phuong_sai_nhieu / phuong_sai_cuc_bo) * (padded_img[i,j] - gia_tri_TB_cuc_bo))
    return img_ket_qua_anh_loc

if __name__ == "__main__":
    img_nhieu = cv2.imread('Anh_nhieu_de_loc_thich_nghi_cuc_bo.tif', 0)
    phuong_sai_nhieu = 0.15
    ksize = 7

    img_ket_qua = Loc_Thich_Nghi_Cuc_Bo(img_nhieu, ksize, phuong_sai_nhieu)

    fig = plt.figure(figsize=(16, 9))     # Thiết lập vùng (cửa sổ) vẽ
    ax1, ax2 = fig.subplots(1, 2)        # Thiết lập 2 vùng con ax1, ax2
    ax1.imshow(img_nhieu, cmap='gray')      # Hiển thị ảnh gốc vùng ax1
    ax1.set_title("ảnh nhiễu Gaussian")             # Thiết lập tiêu đề vùng ax1
    ax1.axis("off")

    ax2.imshow(img_ket_qua, cmap='gray')       # Hiển thị ảnh sau khi lọc
    ax2.set_title("ảnh sau khi qua Bộ lọc thích nghi cục bộ") # Thiết lập tiêu đề vùng ax2
    ax2.axis("off")
    plt.show()