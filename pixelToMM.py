# Tính diện tính của vật thể dựa vào pixel và thước chuẩn
import numpy as np

from objectContour import getFilledContourMask
from imgLoad import loadImage
from scaleCalibration import show_ruler_and_get_scale

def get_object_area(contour_mask, mm_per_pixel):
    # contour_mask: ảnh mask nhị phân (0 và 255), vật thể = 255
    # mm_per_pixel: số mm tương ứng với 1 pixel
    # Trả về diện tích vật thể theo đơn vị mm2

    # Ép về dạng 0 - 255 
    contour_mask = (contour_mask > 0).astype(np.uint8) * 255
    # Đếm số pixel trắng (pixel thể hiện object)
    pixel_area = np.sum(contour_mask == 255)
    #print("Pixel area = :", pixel_area)

    # Quy đổi sang mm2
    real_area = pixel_area * (mm_per_pixel * mm_per_pixel)

    return real_area

# Hàm tự nấu contour và tính diện tích trả về cho gradio
def get_object_area_gradio(obj, mm_per_pixel):
    if obj is None:
        return "Lỗi: object rỗng"

    if mm_per_pixel is None:
        return "Lỗi: mm_per_pixel rỗng"

    # Tạo mask
    mask = getFilledContourMask(obj)

    # Kiểm tra xem mask có vùng trắng không
    white_pixels = np.sum(mask == 255)
    if white_pixels == 0:
        return "Lỗi: Không tìm thấy vật thể trong ảnh"

    try:
        objectArea = get_object_area(mask, mm_per_pixel)
        return f"Diện tích = {objectArea:.2f} mm2"
    except Exception as e:
        return f"ERROR: {str(e)}"

# ruler, obj, full = loadImage("./imgs/earphone2.jpg")

# # Tính giá trị mm mỗi pixel
# mmPerPixel = show_ruler_and_get_scale(ruler)

# objectArea = get_object_area_gradio(obj, mmPerPixel)
# print("Dien tich vat the:", objectArea, "mm2")