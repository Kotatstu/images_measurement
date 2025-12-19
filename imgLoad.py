# Load và tiền xử lý ảnh
# Mục tiêu là giảm nhiễu, xác định contour chính xác hơn

# Resize ảnh.
# Chuyển sang grayscale
# Gaussian blur
# Làm tăng tương phản nếu cần: CLAHE (cv2.createCLAHE()).
# Edge detection: Canny (cv2.Canny(blurred, 50, 150)), hoặc threshold (adaptive).

import cv2
import numpy as np
from PIL import Image

# 1. Hàm resize mới: Giữ nguyên tỷ lệ để vật thể không bị méo
def resize_maintain_aspect(image, target_width=500):
    h, w = image.shape[:2]
    # Tính tỷ lệ scale dựa trên chiều rộng
    scale = target_width / float(w)
    target_height = int(h * scale)
    return cv2.resize(image, (target_width, target_height))

# Hàm load ảnh theo grayscale, xử lý ảnh và trả về thước chuẩn + vật thể + full ảnh
def loadImage(source):
    img = cv2.imread(source, 0)
    if img is None: return None, None, None
    
    img = resize_maintain_aspect(img, 500)

    h = img.shape[0]
    split_point = int(h * 0.2) 

    ruler = img[0:split_point, :]
    object = img[split_point:h, :]

    return ruler, object, img

# background estimation + illumination compensation code tham khảo trên stack overflow
def removeObjectShadow(obj):
    rgb_planes = cv2.split(obj)

    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        
               # shadow = cv2.absdiff(plane, bg_img)
        # diff_img = cv2.subtract(plane, shadow//2)
        
        norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_norm_planes.append(norm_img)
        
    result_norm = cv2.merge(result_norm_planes)
    return result_norm

def load_image_gradio(img_pil):
    if img_pil is None:
        return None, None

    img = np.array(img_pil)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Thay thế resize và cắt 20%
    gray = resize_maintain_aspect(gray, 500)
    h = gray.shape[0]
    split_point = int(h * 0.2)

    ruler = gray[0:split_point, :]
    object = gray[split_point:h, :]

    return ruler, object

def load_image_gradio_ruler(img_pil):
    if img_pil is None:
        return None

    img = np.array(img_pil)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    gray = resize_maintain_aspect(gray, 500)
    h = gray.shape[0]
    split_point = int(h * 0.2)
    
    ruler = gray[0:split_point, :]
    ruler_pil = Image.fromarray(ruler)

    return ruler_pil

# Test hàm
# ruler, object, _ = loadImage('./imgs/earphone.jpg')

# cv2.imshow('Anh thuoc', ruler)
# cv2.waitKey(0)

# cv2.imshow('Anh vat', object)
# cv2.waitKey(0)
# result, result_norm = removeObjectShadow(object)
# cv2.imshow('Anh vat', result_norm)
# cv2.waitKey(0)

# cv2.destroyAllWindows()