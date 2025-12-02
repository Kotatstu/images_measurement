# Tính diện tính của vật thể dựa vào pixel và thước chuẩn
import numpy as np

def get_object_area(contour_mask, mm_per_pixel):
    # contour_mask: ảnh mask nhị phân (0 và 255), vật thể = 255
    # mm_per_pixel: số mm tương ứng với 1 pixel
    # Trả về diện tích vật thể theo đơn vị mm2

    # Ép về dạng 0 - 255 
    contour_mask = (contour_mask > 0).astype(np.uint8) * 255
    # Đếm số pixel trắng (pixel thể hiện object)
    pixel_area = np.sum(contour_mask == 255)
    print("Pixel area = :", pixel_area)

    # Quy đổi sang mm2
    real_area = pixel_area * (mm_per_pixel * mm_per_pixel)

    return real_area