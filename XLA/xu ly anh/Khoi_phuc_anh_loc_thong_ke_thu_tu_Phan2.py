import numpy as np
import cv2
import matplotlib.pyplot as plt


def Loc_TKTT_Midpoint(img, ksize):
    m, n = img.shape
    img_ket_qua_anh_loc_Midpoint = np.zeros([m, n])
    h=(ksize -1) // 2
    padded_img = np.pad(img, (h, h), mode='reflect')
    for i in range(m):
        for j in range(n):
            vung_anh_kich_thuoc_k = padded_img[i:i+ksize,j:j+ksize]
            gia_tri_Max = np.max(vung_anh_kich_thuoc_k)
            gia_tri_Min = np.min(vung_anh_kich_thuoc_k)
            img_ket_qua_anh_loc_Midpoint[i, j] = (gia_tri_Max + gia_tri_Min)/2
    return img_ket_qua_anh_loc_Midpoint

def Loc_Trung_binh_cat_Alpha(img, ksize, alpha):
    m,n = img.shape
    img_LQ_Trung_binh_cat_Alpha = np.zeros([m, n])
    h = (ksize - 1) // 2
    d = int(ksize*ksize*alpha)
    padded_img = np.pad(img,(h,h),mode='reflect')
    for i in range(m):
        for j in range(n):
            vung_anh_kich_thuoc_k = padded_img[i:i+ksize,j:j+ksize].flatten()
            vung_anh_kich_thuoc_k.sort()
            vung_anh_kich_thuoc_con_lai = vung_anh_kich_thuoc_k[d//2:-d//2]
            img_LQ_Trung_binh_cat_Alpha[i,j] = np.sum(vung_anh_kich_thuoc_con_lai) / (m*n-d)
    return img_LQ_Trung_binh_cat_Alpha

if __name__ == "__main__":

    img_nhieu_hat_tieu = cv2.imread('Anh_nhieu_hat_tieu.tif', 0)
    img_nhieu_muoi = cv2.imread('Anh_nhieu_muoi.tif', 0)
    img_nhieu_dong_nhat = cv2.imread('Anh_nhieu_DN_de_loc_MidPoint.tif', 0)
    ksize = 5 # Để lọc ảnh Midpoint
    alpha = 0.25

    img_KQ_MidPoint= Loc_TKTT_Midpoint(img_nhieu_dong_nhat , ksize)
    img_KQ_TBCA = Loc_Trung_binh_cat_Alpha(img_nhieu_dong_nhat, ksize, alpha)

    fig = plt.figure(figsize=(16, 9))     # Thiết lập vùng (cửa sổ) vẽ
    (ax1, ax2), (ax3,ax4) = fig.subplots(2, 2)        # Thiết lập 2 vùng con ax1, ax2
    ax1.imshow(img_nhieu_dong_nhat, cmap='gray')      # Hiển thị ảnh gốc vùng ax1
    ax1.set_title("ảnh gốc bị nhiễu đồng nhất")             # Thiết lập tiêu đề vùng ax1
    ax1.axis("off")

    ax2.imshow(img_KQ_MidPoint, cmap='gray')       # Hiển thị ảnh sau khi lọc
    ax2.set_title("ảnh sau khi lọc MidPoint") # Thiết lập tiêu đề vùng ax2
    ax2.axis("off")

    ax3.axis("off")

    ax4.imshow(img_KQ_TBCA, cmap='gray')  # Hiển thị ảnh sau khi lọc
    ax4.set_title("ảnh sau khi lọc cắt TB Alpha")  # Thiết lập tiêu đề vùng ax2
    ax4.axis("off")

    plt.show()