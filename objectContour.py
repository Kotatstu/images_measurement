# Dùng find contour và các dạng object detection để tìm và đưa ra ảnh contour của vật thể

import cv2
import numpy as np

# Code gần như y hệt code contour thầy hướng dẫn
def getFilledContourMask(gray_img):
    # 1. Khử nhiễu nhưng giữ cạnh sắc nét (thay cho GaussianBlur)
    # Bilateral Filter giúp tính diện tích chính xác hơn ở đường biên
    blurred = cv2.bilateralFilter(gray_img, 9, 75, 75)

    # 2. Nhị phân hóa tự động bằng phương pháp Otsu
    # cv2.THRESH_OTSU tự động tìm ngưỡng tối ưu giữa vật thể và nền
    _, thres = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 3. Bước DILATED (Giãn nở)
    # Mục tiêu: Làm các phần bị khuyết hoặc đứt gãy trong vật thể dính liền lại
    kernel = np.ones((5, 5), dtype='uint8')
    dilated = cv2.dilate(thres, kernel, iterations=1)

    # 4. Bước PROCESS (Xử lý lọc nhiễu)
    # Sử dụng phép Opening để xóa các đốm trắng nhỏ dư thừa phát sinh sau khi Dilate
    processed = cv2.morphologyEx(dilated, cv2.MORPH_OPEN, kernel, iterations=1)

    # 5. Tìm các contour
    contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Tạo ảnh đen để vẽ mask
    contourImg = np.zeros_like(gray_img)

    # 6. Chỉ chọn và vẽ vật thể lớn nhất
    if contours:
        # Tìm contour có diện tích lớn nhất (bỏ qua các vật thể rác)
        largest_contour = max(contours, key=cv2.contourArea)
        # Fill vật thể bằng màu trắng
        cv2.drawContours(contourImg, [largest_contour], -1, (255, 255, 255), thickness=cv2.FILLED)

    return contourImg

# img = cv2.imread("./imgs/earphone.jpg", 1)
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# contourImg = getFilledContourMask(gray)
# contourImg = cv2.resize(contourImg, (500, 500))

# cv2.imshow("Contour", contourImg)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

