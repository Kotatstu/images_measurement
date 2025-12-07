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

# Hàm load ảnh theo grayscale, xử lý ảnh và trả về thước chuẩn + vật thể + full ảnh
def loadImage(source):
    img = cv2.imread(source, 0)
    img = cv2.resize(img, (500, 500))
    

    ruler = img[0:100, :]
    object = img[100:500, :]

    #object = cv2.GaussianBlur(object, (5, 5), 0)

    return ruler, object, img

# background estimation + illumination compensation code tham khảo trên stack overflow
def removeObjectShadow(obj):
    rgb_planes = cv2.split(obj)

    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))

        bg_img = cv2.medianBlur(dilated_img, 21)

        diff_img = 255 - cv2.absdiff(plane, bg_img)
        # shadow = cv2.absdiff(plane, bg_img)
        # diff_img = cv2.subtract(plane, shadow//2)

        norm_img = cv2.normalize(diff_img,None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_planes.append(diff_img)
        result_norm_planes.append(norm_img)
        
    result = cv2.merge(result_planes)
    result_norm = cv2.merge(result_norm_planes)

    return result, result_norm

def load_image_gradio(img_pil):

    if img_pil is None:
        return None, None

    img = np.array(img_pil)

    # Convert sang gray bằng OpenCV
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Resize chuẩn
    gray = cv2.resize(gray, (500, 500))

    # Tách ảnh
    ruler = gray[0:100, :]
    object = gray[100:500, :]

    return ruler, object

def load_image_gradio_ruler(img_pil):
    
    if img_pil is None:
        return None, None

    img = np.array(img_pil)

    # Convert sang gray bằng OpenCV
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Resize chuẩn
    gray = cv2.resize(gray, (500, 500))

    # Tách ảnh
    ruler = gray[0:100, :]


    # Convert ngược lại sang PIL để render trên giao diện
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