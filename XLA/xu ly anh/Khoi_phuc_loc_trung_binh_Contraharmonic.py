import numpy as np
import cv2
import matplotlib.pyplot as plt

def Loc_Trung_binh_Contraharmonic(img, ksize,Q):
    m, n = img.shape
    img_ket_qua_anh_loc = np.zeros([m, n])

    h=(ksize -1) // 2
    padded_img = np.pad(img, (h, h), mode='reflect')
    padded_img_bac_Q_cong_1 = np.power(padded_img, Q+1)
    padded_img_bac_Q = np.power(padded_img, Q)

    for i in range(m):
        for j in range(n):
            vung_anh_kich_thuoc_k_bac_Q_cong_1 = padded_img_bac_Q_cong_1[i:i+ksize,j:j+ksize]
            vung_anh_kich_thuoc_k_bac_Q = padded_img_bac_Q[i:i + ksize, j:j + ksize]
            img_bac_Q_1 = np.sum(vung_anh_kich_thuoc_k_bac_Q_cong_1)
            img_bac_Q = np.sum(vung_anh_kich_thuoc_k_bac_Q)
            gia_tri_loc = img_bac_Q_1/img_bac_Q
            img_ket_qua_anh_loc[i, j] = gia_tri_loc
    return img_ket_qua_anh_loc

if __name__ == "__main__":
    img_nhieu_hat_tieu = cv2.imread('Anh_nhieu_hat_tieu.tif', 0)
    img_nhieu_muoi = cv2.imread('Anh_nhieu_muoi.tif', 0)
    ksize =3
    Q1=1.5
    Q2 = -.8
    img_ket_qua_TBContraharmonic1=Loc_Trung_binh_Contraharmonic(img_nhieu_hat_tieu, ksize,Q1)
    img_ket_qua_TBContraharmonic2 = Loc_Trung_binh_Contraharmonic(img_nhieu_muoi, ksize, Q2)
    fig = plt.figure(figsize=(16, 9))     # Thiết lập vùng (cửa sổ) vẽ
    (ax1, ax2),(ax3,ax4) = fig.subplots(2, 2)        # Thiết lập 2 vùng con ax1, ax2
    ax1.imshow(img_nhieu_hat_tieu, cmap='gray')      # Hiển thị ảnh gốc vùng ax1
    ax1.set_title("ảnh gốc bị nhiễu hạt tiêu")             # Thiết lập tiêu đề vùng ax1
    ax1.axis("off")

    ax2.imshow(img_ket_qua_TBContraharmonic1, cmap='gray')  # Hiển thị ảnh sau khi lọc
    ax2.set_title("ảnh sau khi lọc Trung bình Contraharmonic")  # Thiết lập tiêu đề vùng ax2
    ax2.axis("off")

    ax3.imshow(img_nhieu_muoi, cmap='gray')  # Hiển thị ảnh gốc vùng ax3
    ax3.set_title("ảnh gốc bị nhiễu muối")  # Thiết lập tiêu đề vùng ax3
    ax3.axis("off")

    ax4.imshow(img_ket_qua_TBContraharmonic2, cmap='gray')  # Hiển thị ảnh sau khi lọc
    ax4.set_title("ảnh sau khi lọc Trung bình Contraharmonic")  # Thiết lập tiêu đề vùng ax4
    ax4.axis("off")

    plt.show()