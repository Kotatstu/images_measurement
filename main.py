# Các bước chính:
# 1. Ảnh đầu vào gồm 1 vật thể mình muốn đo và 1 thước chuẩn để làm mốc tính pixel -> mm. Đọc ảnh và tiền xử lý ảnh.
# 2. Đọc cái thước chuẩn
# 3. Calibration để chuẩn hóa về 1 mặt phẳng, đo chính xác hơn
# 4. Phát hiện được vật thể ở đâu trên hình
# 5. Tính diện tích của vật thể sau khi xác định kích thước chuẩn và vật thể
# 6. Chạy main.py, hiển thị kết quả

import cv2
import numpy as np

from imgLoad import loadImage
from scaleCalibration import show_ruler_and_get_scale
from objectContour import getFilledContourMask
from pixelToMM import get_object_area

# Load và xử lý ảnh đầu vào
ruler, obj, full = loadImage("./imgs/earphone2.jpg")
# print("Kich thuoc anh thuoc: ", ruler.size)
# print("Kich thuoc anh vat the: ", obj.size)
# print("Kich thuoc anh full", full.size)

cv2.imshow("Anh vat the", obj)
cv2.waitKey(0)


# Tính giá trị mm mỗi pixel
mmPerPixel = show_ruler_and_get_scale(ruler)


# Tìm contour
mask = getFilledContourMask(obj)


# Tính diện tích vật thể
objectArea = get_object_area(mask, mmPerPixel)
print("Dien tich vat the:", objectArea, "mm2")


contourImg = cv2.resize(mask, (500, 500))
cv2.imshow("Contour", contourImg)
cv2.waitKey(0)


cv2.destroyAllWindows()