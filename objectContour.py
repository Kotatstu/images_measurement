# Dùng find contour và các dạng object detection để tìm và đưa ra ảnh contour của vật thể

import cv2
import numpy as np

# Code gần như y hệt code contour thầy hướng dẫn
def getFilledContourMask(gray_img):
    # 1. Làm mờ giảm nhiễu
    blurred = cv2.GaussianBlur(gray_img, (11, 11), 0)

    # 2. Nhị phân hóa
    _, thres = cv2.threshold(blurred, 70, 255, cv2.THRESH_BINARY_INV) # THRESH_OTSU dùng để tự động chọn ngưỡng (+ cv2.THRESH_OTSU)

    # 3. Morphology làm rõ vùng
    kernel = np.ones((3, 3), dtype='uint8')
    dilated = cv2.dilate(thres, kernel, iterations=3)
    processed = cv2.erode(dilated, kernel, iterations=2)

    # 4. Tìm contour
    contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Tạo ảnh full đen
    contourImg = np.zeros_like(gray_img)

    if contours:
        # 4. Tìm contour có diện tích lớn nhất
        largest_contour = max(contours, key=cv2.contourArea)
        
        # 5. Vẽ và lấp đầy (fill) duy nhất contour lớn nhất đó
        # thickness=cv2.FILLED hoặc -1 sẽ tô màu trắng toàn bộ vùng bên trong
        cv2.drawContours(contourImg, [largest_contour], -1, 255, thickness=cv2.FILLED)

    return contourImg

# img = cv2.imread("./imgs/earphone.jpg", 1)
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# contourImg = getFilledContourMask(gray)
# contourImg = cv2.resize(contourImg, (500, 500))

# cv2.imshow("Contour", contourImg)
# cv2.waitKey(0)
# cv2.destroyAllWindows()