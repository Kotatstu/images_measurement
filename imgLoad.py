# Load và tiền xử lý ảnh
# Mục tiêu là giảm nhiễu, xác định contour chính xác hơn

# Resize ảnh.
# Chuyển sang grayscale
# Gaussian blur
# Làm tăng tương phản nếu cần: CLAHE (cv2.createCLAHE()).
# Edge detection: Canny (cv2.Canny(blurred, 50, 150)), hoặc threshold (adaptive).

import cv2

# Hàm load ảnh theo grayscale, xử lý ảnh và trả về thước chuẩn + vật thể + full ảnh
def loadImage(source):
    img = cv2.imread(source, 0)
    img = cv2.resize(img, (500, 500))
    

    ruler = img[0:100, :]
    object = img[100:500, :]

    #object = cv2.GaussianBlur(object, (5, 5), 0)

    return ruler, object, img



# Test hàm
# ruler, object, _ = loadImage('./imgs/earphone.jpg')

# cv2.imshow('Anh thuoc', ruler)
# cv2.waitKey(0)

# cv2.imshow('Anh thuoc', object)
# cv2.waitKey(0)

# cv2.destroyAllWindows()